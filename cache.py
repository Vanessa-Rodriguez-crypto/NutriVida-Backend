import time

cache = {}

def guardar_cache(clave, valor, segundos=60):
    cache[clave] = {
        "valor": valor,
        "expira": time.time() + segundos
    }


def obtener_cache(clave):
    dato = cache.get(clave)

    if dato:
        if time.time() < dato["expira"]:
            return dato["valor"]
        else:
            del cache[clave]

    return None


def eliminar_cache(clave):
    if clave in cache:
        del cache[clave]