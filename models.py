from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    objetivos = db.relationship(
        "Objetivo",
        backref="usuario",
        lazy=True
    )


class Objetivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peso_meta = db.Column(db.Float, nullable=False)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )


class Alimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    calorias = db.Column(db.Float)
    proteinas = db.Column(db.Float)
    carbohidratos = db.Column(db.Float)