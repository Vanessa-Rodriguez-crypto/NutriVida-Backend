import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "NutriVida-clave-segura-2026-32bytes!")
    SQLALCHEMY_DATABASE_URI = "sqlite:///nutrivida.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
