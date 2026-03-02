from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Juego:
    nombre: str
    genero: str
    fecha: datetime
    descripcion: str
    caratula: Optional[str] = None
    horas: float = 0.0
    logros: Optional[List[str]] = None
    plataforma: Optional[str] = None

    def agregar_horas(self, cantidad: float):
        if cantidad < 0:
            raise ValueError("La cantidad de horas no puede ser negativa.")
        self.horas += cantidad