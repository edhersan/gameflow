import os

BASE_DIR = os.path.join(os.path.expanduser("~"), ".gameflow")

DB_PATH = os.path.join(BASE_DIR, "gameflow.db")

CARATULAS_DIR = os.path.join(BASE_DIR, "caratulas")

def asegurar_estructura():
    print(">>> Creando carpetas .gameflow ...")
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(CARATULAS_DIR, exist_ok=True)