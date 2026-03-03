from pydantic import BaseModel
from typing import Optional

# Modelos de datos para la API de juegos
class JuegoIn(BaseModel):
    nombre: str
    genero: str
    fecha: Optional[str] = None  # 'YYYY-MM-DD'
    descripcion: Optional[str] = None
    caratula: Optional[str] = None
    horas: Optional[float] = 0
    logros: Optional[str] = None
    plataforma: Optional[str] = None

class JuegoOut(JuegoIn):
    id: int