import os
import requests

from fastapi import FastAPI, HTTPException
from database import inicializar_bd, obtener_conexion
from models import JuegoIn, JuegoOut
from config import asegurar_estructura, CARATULAS_DIR
from external_covers import buscar_caratula_por_titulo

app = FastAPI()

# Este evento se ejecuta al iniciar la aplicación, y se encarga de inicializar la base de datos
@app.on_event("startup")
def startup_event():
    asegurar_estructura()  # Aseguramos que la estructura de carpetas exista
    inicializar_bd()

@app.get("/")
def read_root():
    return {"mensaje": "Esta api ya esta funcionando"}

# Endpoint para listar todos los juegos
@app.get("/juegos")
def listar_juegos():
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("SELECT * FROM juegos")
    filas = cur.fetchall()
    conn.close()
# Convertir las filas obtenidas en una lista de diccionarios para facilitar su uso en la respuesta JSON
    juegos = []
    for fila in filas:
        juegos.append  ({
            "id": fila["id"],
            "nombre": fila["nombre"],
            "genero": fila["genero"],
            "fecha": fila["fecha"],
            "descripcion": fila["descripcion"],
            "caratula": fila["caratula"],
            "horas": fila["horas"],
            "logros": fila["logros"],
            "plataforma": fila["plataforma"]
        })
    return juegos

# Endpoint para agregar un nuevo juego
@app.post("/juegos", response_model=JuegoOut)
def agregar_juego(juego: JuegoIn):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO juegos (nombre, genero, fecha, descripcion, caratula, horas, logros, plataforma)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
          juego.nombre, 
          juego.genero, 
          juego.fecha, 
          juego.descripcion, 
          juego.caratula, 
          juego.horas, 
          juego.logros, 
          juego.plataforma
          ))
    conn.commit()
    id_juego = cur.lastrowid
    conn.close()
    
    return JuegoOut(id=id_juego, **juego.dict())

# Endpoint para actualizar un juego existente
@app.put("/juegos/{id_juego}", response_model=JuegoOut)
def actualizar_juego(id_juego: int, juego: JuegoIn):
    conn = obtener_conexion()
    cur = conn.cursor()
# Primero verificamos si el juego existe para evitar actualizar un registro que no existe
    cur.execute("SELECT * FROM juegos WHERE id = ?", (id_juego,))
    existente = cur.fetchone()
    if existente is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Juego no encontrado")  
 # Si el juego existe, procedemos a actualizarlo con los nuevos datos proporcionados   
    cur.execute("""
        UPDATE juegos
        SET nombre = ?, genero = ?, fecha = ?, descripcion = ?, caratula = ?, horas = ?, logros = ?, plataforma = ?
        WHERE id = ?
    """, (
          juego.nombre, 
          juego.genero, 
          juego.fecha, 
          juego.descripcion, 
          juego.caratula, 
          juego.horas, 
          juego.logros, 
          juego.plataforma,
          id_juego
          ))
    conn.commit()
    conn.close()
    
    return JuegoOut(id=id_juego, **juego.dict())

# Endpoint para eliminar un juego
@app.delete("/juegos/{id_juego}")
def eliminar_juego(id_juego: int):
    conn = obtener_conexion()
    cur = conn.cursor()
# Verificamos si el juego existe antes de intentar eliminarlo
    cur.execute("SELECT * FROM juegos WHERE id = ?", (id_juego,))
    existente = cur.fetchone()
    if existente is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Juego no encontrado")
# Si el juego existe, procedemos a eliminarlo
    cur.execute("DELETE FROM juegos WHERE id = ?", (id_juego,))
    conn.commit()
    conn.close()
    return {"mensaje": "Juego eliminado exitosamente, ya no esta, se fue"}

# Endpoint para descargar automáticamente la carátula de un juego utilizando su título
@app.post("/juegos/{id_juego}/caratula/auto", response_model=JuegoOut)
def descargar_caratula_auto(id_juego: int):
    conn = obtener_conexion()
    cur = conn.cursor()

# Primero verificamos si el juego existe
    cur.execute("SELECT * FROM juegos WHERE id = ?", (id_juego,))
    fila = cur.fetchone()
    if fila is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    titulo = fila["nombre"]

    url_imagen = buscar_caratula_por_titulo(titulo)
    if not url_imagen:
        conn.close()
        raise HTTPException(status_code=404, detail="No se encontró una carátula para este juego")
    try:
        resp = requests.get(url_imagen, timeout=15)
    except requests.RequestException:
        conn.close()
        raise HTTPException(status_code=502, detail="Error al conectar con RAWG") 
    if resp.status_code != 200:
        conn.close()
        raise HTTPException(status_code=502, detail="Error al descargar  la carátula") 
    
    os.makedirs(CARATULAS_DIR, exist_ok=True)

    nombre_archivo = f"{id_juego}.jpg"
    ruta_archivo = os.path.join(CARATULAS_DIR, nombre_archivo)
    with open(ruta_archivo, "wb") as f:
         f.write(resp.content)

    ruta_guardada = os.path.join(CARATULAS_DIR, nombre_archivo)
    cur.execute("UPDATE juegos SET caratula = ? WHERE id = ?", (ruta_guardada, id_juego))
    conn.commit()
    conn.close()
    return JuegoOut(
        id= fila["id"],
        nombre= fila["nombre"],
        genero= fila["genero"],
        fecha= fila["fecha"],
        descripcion= fila["descripcion"],
        caratula= ruta_guardada,
        horas= fila["horas"],
        logros= fila["logros"],
        plataforma= fila["plataforma"]
    )