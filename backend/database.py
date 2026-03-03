import os
import sqlite3
from sqlite3 import Connection
from config import DB_PATH

#devuelve la ruta absoluta del archivo de la base de datos
def obtener_ruta_bd() -> str:
    capeta_actual = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(capeta_actual, "gameflow.db")

#devuelve una conexion a la base de datos
def obtener_conexion() -> Connection:
    ruta_bd = obtener_ruta_bd()
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_bd()-> None:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS juegos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        genero TEXT NOT NULL,
        fecha TEXT,     --la guardaremos como 'YYYY-MM-DD'
        descripcion TEXT,
        caratula TEXT,
        horas REAL DEFAULT 0,
        logros TEXT,
        plataforma TEXT
    );
    """)
        
    conexion.commit()
    conexion.close()