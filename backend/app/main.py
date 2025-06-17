from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user, application, interaction    # importa tu router
from app.core.dependencies import get_current_user

# Inicializar la app
app = FastAPI()

# CORS: permite enviar cookies (credenciales)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # tu front
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
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

# Rutas públicas
app.include_router(auth.router)

# Rutas protegidas: inyectan get_current_user
app.include_router(user.router, dependencies=[Depends(get_current_user)])
app.include_router(application.router, dependencies=[Depends(get_current_user)])
app.include_router(interaction.router, dependencies=[Depends(get_current_user)])