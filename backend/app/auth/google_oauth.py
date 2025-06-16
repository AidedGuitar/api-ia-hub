# app/auth/google_oauth.py
import requests
from fastapi import HTTPException, status
from app.config import settings

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

def verify_google_token(id_token: str) -> dict:
    resp = requests.get(GOOGLE_TOKEN_INFO_URL, params={"id_token": id_token})
    if resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ID token inválido")
    data = resp.json()
    if data.get("aud") != settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token para otro cliente")
    return data  # contiene email, name, picture…
