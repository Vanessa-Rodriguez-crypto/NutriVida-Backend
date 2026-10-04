import os

class Config:
    SECRET_KEY = "nutrivida-secreto"
    SQLALCHEMY_DATABASE_URI = "sqlite:///nutrivida.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False