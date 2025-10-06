from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.models_sqlalchemy import User, Application, Feedback

class ContentBasedRecommender:
    def __init__(self, db: Session):
        self.db = db
        self.applications_df = None
        self.tfidf_matrix = None
        self._load_data()
        self._build_model()

    def _load_data(self):
        # Cargar todas las materias/aplicaciones desde la BD
        applications = self.db.query(Application).all()
        self.applications_df = pd.DataFrame([
            {
                'id': str(app.id),
                'name': app.app_name,
                'category': app.app_category or "",
                'description': app.app_description or "",
                'keywords': getattr(app, 'app_keywords', "") or "",
                'academic_level': getattr(app, 'app_academic_level', "") or "",
                'credits': getattr(app, 'app_credits', 0)
            }
            for app in applications
        ])

    def _build_model(self):
        # Crear una "firma" de texto combinando campos relevantes
        self.applications_df['combined_features'] = (
            self.applications_df['category'] + " " +
            self.applications_df['description'] + " " +
            self.applications_df['keywords'] + " " +
            self.applications_df['academic_level']
        )
        # Vectorizar con TF-IDF
        tfidf = TfidfVectorizer(stop_words='spanish')  # o 'english' si usas inglés
        self.tfidf_matrix = tfidf.fit_transform(self.applications_df['combined_features'])

    def recommend(self, user_id: str, top_n: int = 5) -> List[Dict]:
        # Paso 1: Obtener las aplicaciones que el usuario ha calificado positivamente (rating >= 4)
        feedbacks = self.db.query(Feedback).filter(
            Feedback.user_id == user_id,
            Feedback.fee_rating >= 4
        ).all()

        if not feedbacks:
            # Si no hay historial, devolver las más populares o por defecto
            return self._get_default_recommendations(top_n)

        liked_app_ids = [str(f.application_id) for f in feedbacks]
        liked_indices = self.applications_df[
            self.applications_df['id'].isin(liked_app_ids)
        ].index.tolist()

        # Paso 2: Calcular similitud
        if liked_indices:
            user_profile = self.tfidf_matrix[liked_indices].mean(axis=0)
            sim_scores = cosine_similarity(user_profile, self.tfidf_matrix).flatten()
        else:
            sim_scores = [0] * len(self.applications_df)

        # Paso 3: Ordenar y excluir ya vistas
        self.applications_df['sim_score'] = sim_scores
        recommendations = self.applications_df.sort_values('sim_score', ascending=False)
        recommendations = recommendations[~recommendations['id'].isin(liked_app_ids)]

        return recommendations.head(top_n).to_dict('records')

    def _get_default_recommendations(self, top_n: int) -> List[Dict]:
        # Recomendación por defecto: las primeras N aplicaciones
        return self.applications_df.head(top_n).to_dict('records')