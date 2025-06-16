from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DB, otros…
    DATABASE_URL: str
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 día

    COOKIE_NAME: str = "access_token"
    COOKIE_DOMAIN: str = "localhost"          # ajusta a tu dominio
    COOKIE_SECURE: bool = False               # True en producción (HTTPS)
    COOKIE_SAMESITE: str = "lax"

    GOOGLE_CLIENT_ID: str

    class Config:
        env_file = ".env"

settings = Settings()