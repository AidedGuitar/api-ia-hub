# app/recommender/content_recommender.py
from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.models_sqlalchemy import Application, Feedback, Interaction
from datetime import datetime, timedelta
import threading

# Pesos por tipo de interacción (ajustables)
DEFAULT_INTERACTION_WEIGHTS = {
    "view": 0.2,
    "click": 0.5,
    "favorite": 0.8,
    # rating/feedback será manejado por fee_rating; pero si hay int_type 'feedback' le damos un peso:
    "feedback": 1.0
}

class ContentBasedRecommender:
    """
    Recomendador content-based con:
      - TF-IDF sobre campos textuales de Application
      - perfil de usuario derivado de interacciones ponderadas
      - integración del rating promedio de la app en el score final
    """

    _instance_lock = threading.Lock()
    _instance = None

    def __init__(self, db: Session, interaction_weights: dict = None, rating_weight: float = 0.3,
                 exclude_already_interacted: bool = True, min_avg_rating: float = 0.0):
        """
        rating_weight: cuánto pesa el promedio de rating [0..1] en el score final.
        exclude_already_interacted: si True excluye apps ya interaccionadas por el usuario.
        min_avg_rating: apps con promedio por debajo de esto serán excluidas (o filtradas).
        """
        self.db = db
        self.interaction_weights = interaction_weights or DEFAULT_INTERACTION_WEIGHTS
        self.rating_weight = float(rating_weight)
        self.exclude_already_interacted = bool(exclude_already_interacted)
        self.min_avg_rating = float(min_avg_rating)

        # Cache interno
        self.applications_df: Optional[pd.DataFrame] = None
        self.tfidf_matrix = None
        self.tfidf_vectorizer: Optional[TfidfVectorizer] = None
        self._last_built = None

        # Construir por primera vez
        self.refresh()

    # -------------------------
    # Carga y construcción
    # -------------------------
    def _load_data(self):
        apps = self.db.query(Application).all()
        rows = []
        for app in apps:
            rows.append({
                "id": str(app.id),
                "app_name": app.app_name or "",
                "app_category": app.app_category or "",
                "app_description": app.app_description or "",
                "app_keywords": (app.app_keywords or ""),
                "app_academic_level": (app.app_academic_level or ""),
                "app_link": app.app_link or "",
            })
        self.applications_df = pd.DataFrame(rows)

        # Si no hay apps, dejar df vacío para evitar errores posteriores
        if self.applications_df.empty:
            self.applications_df = pd.DataFrame(columns=[
                "id","app_name","app_category","app_description","app_keywords","app_academic_level","app_link"
            ])

    def _build_tfidf(self):
        # concatenar campos relevantes
        self.applications_df["combined_features"] = (
            self.applications_df["app_category"].fillna("") + " " +
            self.applications_df["app_description"].fillna("") + " " +
            self.applications_df["app_keywords"].fillna("") + " " +
            self.applications_df["app_academic_level"].fillna("")
        )
        self.tfidf_vectorizer = TfidfVectorizer(stop_words=None)
        # Si dataframe vacío, evitar fit_transform con error
        if len(self.applications_df) == 0:
            self.tfidf_matrix = None
            return
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.applications_df["combined_features"])

    def refresh(self):
        """Forzar recarga de datos y reconstrucción del modelo (cache invalidation)."""
        self._load_data()
        self._build_tfidf()
        self._last_built = datetime.utcnow()

    # -------------------------
    # Helpers
    # -------------------------
    def _get_app_avg_ratings(self) -> dict:
        """Retorna dict {app_id: avg_rating}"""
        q = (
            self.db.query(Feedback.application_id, func.avg(Feedback.fee_rating).label("avg"))
            .group_by(Feedback.application_id)
        )
        # imports locales para evitar circular
        results = q.all()
        return {str(row.application_id): float(row.avg) for row in results}

    def _get_user_interactions(self, user_id: str) -> List[dict]:
        """Regresa lista de interactions del usuario (application_id, int_type)."""
        ints = self.db.query(Interaction).filter(Interaction.user_id == user_id).all()
        return [{"application_id": str(i.application_id), "int_type": i.int_type} for i in ints]

    def _get_user_feedbacks(self, user_id: str) -> List[dict]:
        """Retorna feedbacks del usuario (application_id, fee_rating)."""
        fbs = self.db.query(Feedback).filter(Feedback.user_id == user_id).all()
        return [{"application_id": str(f.application_id), "fee_rating": f.fee_rating} for f in fbs]

    # Normaliza array a [0,1]
    @staticmethod
    def _normalize_array(arr: np.ndarray) -> np.ndarray:
        arr = np.array(arr, dtype=float)
        if arr.size == 0:
            return arr
        minv = float(arr.min())
        maxv = float(arr.max())
        if maxv - minv == 0:
            return np.ones_like(arr) * 0.5
        return (arr - minv) / (maxv - minv)

    # -------------------------
    # Recomendación principal
    # -------------------------
    def recommend(self, user_id: str, top_n: int = 5) -> List[Dict]:
        """
        Devuelve lista de apps recomendadas para user_id.
        """
        # Si no hay apps en el sistema, devolver vacío
        if self.applications_df is None or len(self.applications_df) == 0:
            return []

        # 1) Obtener interacción y feedback del usuario
        user_interactions = self._get_user_interactions(user_id)
        user_feedbacks = self._get_user_feedbacks(user_id)
        interacted_app_ids = {i["application_id"] for i in user_interactions}
        feedback_map = {f["application_id"]: f["fee_rating"] for f in user_feedbacks}

        # 2) Determinar apps "liked" para construir perfil
        # Considerar liked por interactions con peso >= 0.5 o por rating >=4
        liked_ids = set()
        for i in user_interactions:
            w = self.interaction_weights.get(i["int_type"], 0.0)
            if w >= 0.5:
                liked_ids.add(i["application_id"])
        for appid, rating in feedback_map.items():
            if rating >= 4:
                liked_ids.add(appid)

        # 3) Si no hay liked, fallback: devolver por rating promedio o por popularidad
        if not liked_ids:
            return self._get_default_recommendations(top_n)

        # 4) Calcular user profile TF-IDF
        liked_indices = self.applications_df[self.applications_df["id"].isin(list(liked_ids))].index.tolist()
        if not liked_indices or self.tfidf_matrix is None:
            return self._get_default_recommendations(top_n)

        user_profile = self.tfidf_matrix[liked_indices].mean(axis=0)  # sparse matrix
        sim_scores = cosine_similarity(user_profile, self.tfidf_matrix).flatten()

        # 5) Integrar promedio de ratings
        # construir vector de avg ratings alineado a self.applications_df rows
        app_avg = self._get_app_avg_ratings()  # {id: avg}
        avg_ratings_vec = np.array([app_avg.get(appid, 0.0) for appid in self.applications_df["id"]], dtype=float)
        # normalizar ratings a 0..1
        norm_ratings = self._normalize_array(avg_ratings_vec)

        # 6) Convertir sim_scores a array y normalizar
        norm_sim = self._normalize_array(sim_scores)

        # 7) Combinar: final_score = (1-rating_weight) * norm_sim + rating_weight * norm_ratings
        final_scores = (1.0 - self.rating_weight) * norm_sim + self.rating_weight * norm_ratings

        # 8) Penalizar apps que el user calificó bajo (<=2) para reducir probabilidad
        penalized = np.array(final_scores)
        for idx, appid in enumerate(self.applications_df["id"]):
            r = feedback_map.get(appid)
            if r is not None and r <= 2:
                penalized[idx] *= 0.2  # penalización fuerte; configurable

        # 9) Excluir apps ya interaccionadas si está configurado
        candidates_df = self.applications_df.copy()
        candidates_df["score"] = penalized

        if self.exclude_already_interacted:
            candidates_df = candidates_df[~candidates_df["id"].isin(interacted_app_ids)]

        # 10) Filtrar por min_avg_rating si estableciste un umbral
        if self.min_avg_rating > 0:
            # map average ratings (no normalizados) y filtrar
            candidates_df["avg_rating"] = [app_avg.get(appid, 0.0) for appid in candidates_df["id"]]
            candidates_df = candidates_df[candidates_df["avg_rating"] >= self.min_avg_rating]

        # 11) Ordenar y devolver top_n con campos limpios
        candidates_df = candidates_df.sort_values("score", ascending=False)
        result = candidates_df.head(top_n)[[
            "id", "app_name", "app_category", "app_description", "app_link", "score"
        ]].to_dict("records")

        # Añadir detalle de avg_rating para info (opcional)
        for r in result:
            r["avg_rating"] = app_avg.get(r["id"], None)

        return result

    def _get_default_recommendations(self, top_n: int) -> List[Dict]:
        # Default: apps por avg rating (desc) y luego por TF-IDF si no hay rating
        app_avg = self._get_app_avg_ratings()
        df = self.applications_df.copy()
        df["avg_rating"] = [app_avg.get(appid, 0.0) for appid in df["id"]]
        df = df.sort_values(["avg_rating"], ascending=False)
        out = df.head(top_n)[[
            "id", "app_name", "app_category", "app_description", "app_link"
        ]].to_dict("records")
        for r in out:
            r["avg_rating"] = app_avg.get(r["id"], None)
        return out
