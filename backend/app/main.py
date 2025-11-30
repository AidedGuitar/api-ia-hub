from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user, application, interaction, feedback, career, recommendation   # importa tu router
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

#ruta raiz
@app.get("/api")
def root():
    return {"message": "Welcome to the Academic Recommender API"}

# Rutas públicas
app.include_router(auth.router)

# Rutas protegidas: inyectan get_current_user
app.include_router(user.router, dependencies=[Depends(get_current_user)])
app.include_router(application.router, dependencies=[Depends(get_current_user)])
app.include_router(interaction.router, dependencies=[Depends(get_current_user)])
app.include_router(feedback.router, dependencies=[Depends(get_current_user)])
app.include_router(career.router, dependencies=[Depends(get_current_user)])
app.include_router(recommendation.router, dependencies=[Depends(get_current_user)])