from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from sqlalchemy.orm import joinedload
import threading
import time

from config import Config
from models import db, Usuario, Objetivo, Alimento
from cache import guardar_cache, obtener_cache

app = Flask(__name__)

app.config.from_object(Config)

# JWT
app.config["JWT_SECRET_KEY"] = "clave-nutrivida-jwt"

jwt = JWTManager(app)

db.init_app(app)


# =====================================
# FUNCIÓN QUE SIMULA UN WORKER
# =====================================
def enviar_correo_simulado(correo):

    print("Enviando correo a:", correo)

    time.sleep(5)

    print("Correo enviado correctamente a:", correo)


@app.route("/")
def inicio():
    return jsonify({
        "mensaje": "API NutriVida funcionando"
    })


# =====================================
# REGISTRO
# =====================================
@app.route("/registro", methods=["POST"])
def registro():

    datos = request.json

    nuevo_usuario = Usuario(
        nombre=datos["nombre"],
        correo=datos["correo"],
        password=datos["password"]
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "mensaje": "Usuario registrado correctamente"
    })


# =====================================
# LOGIN
# =====================================
@app.route("/login", methods=["POST"])
def login():

    datos = request.json

    usuario = Usuario.query.filter_by(
        correo=datos["correo"]
    ).first()

    if usuario and usuario.password == datos["password"]:

        token = create_access_token(
            identity=str(usuario.id)
        )

        return jsonify({
            "token": token
        })

    return jsonify({
        "error": "Credenciales incorrectas"
    }), 401


# =====================================
# PERFIL PROTEGIDO
# =====================================
@app.route("/perfil")
@jwt_required()
def perfil():

    usuario_id = int(get_jwt_identity())

    usuario = Usuario.query.get(usuario_id)

    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "correo": usuario.correo
    })


# =====================================
# CACHE
# =====================================
@app.route("/alimentos", methods=["GET"])
def alimentos():

    datos_cache = obtener_cache("lista_alimentos")

    if datos_cache:
        return jsonify({
            "origen": "cache",
            "datos": datos_cache
        })

    alimentos = Alimento.query.all()

    resultado = []

    for alimento in alimentos:
        resultado.append({
            "id": alimento.id,
            "nombre": alimento.nombre,
            "calorias": alimento.calorias
        })

    guardar_cache(
        "lista_alimentos",
        resultado,
        60
    )

    return jsonify({
        "origen": "base_datos",
        "datos": resultado
    })


# =====================================
# CORRECCIÓN N+1
# =====================================
@app.route("/usuarios_objetivos", methods=["GET"])
def usuarios_objetivos():

    usuarios = Usuario.query.options(
        joinedload(Usuario.objetivos)
    ).all()

    resultado = []

    for usuario in usuarios:

        objetivos = []

        for objetivo in usuario.objetivos:
            objetivos.append({
                "id": objetivo.id,
                "peso_meta": objetivo.peso_meta
            })

        resultado.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "objetivos": objetivos
        })

    return jsonify(resultado)


# =====================================
# COLA DE TRABAJO (WORKER)
# =====================================
@app.route("/enviar_correo", methods=["POST"])
def enviar_correo():

    datos = request.json

    print(f"Enviando correo a: {datos['correo']}", flush=True)

    time.sleep(2)

    print("Correo enviado correctamente", flush=True)

    return jsonify({
        "mensaje": "Correo enviado correctamente."
    })

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)