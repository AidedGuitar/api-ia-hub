from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user    # importa tu router

# Inicializar la app
app = FastAPI()

# Habilitar CORS para que Next.js pueda hacer peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulamos una lista de aplicaciones externas
mock_apps = [
    {"id": 1, "name": "Spotify", "category": "Música"},
    {"id": 2, "name": "Netflix", "category": "Entretenimiento"},
    {"id": 3, "name": "Duolingo", "category": "Educación"},
    {"id": 4, "name": "Asana", "category": "Productividad"},
]

#ruta raiz
@app.get("/api")
def root():
    return {"message": "Welcome to the Academic Recommender API"}

@app.get("/recommendations")
def get_recommendations(user_id: int = 1):
    # Simulamos una recomendación básica (las dos primeras apps)
    return {"user_id": user_id, "recommendations": mock_apps[:2]}

# ⬇️ ESTA LÍNEA es la que debes añadir para registrar el router de auth
app.include_router(auth.router)
app.include_router(user.router)