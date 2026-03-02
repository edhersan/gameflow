from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Juego:
    nombre: str
    genero: str
    fecha: datetime
    descripcion: str
    id: Optional[int] = None
    caratula: Optional[str] = None
    horas: float = 0.0
    logros: Optional[List[str]] = None
    plataforma: Optional[str] = None

    def agregar_horas(self, cantidad: float):
        if cantidad < 0:
            raise ValueError("La cantidad de horas no puede ser negativa.")
        self.horas += cantidad
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "fecha": self.fecha.isoformat(),
            "descripcion": self.descripcion,
            "caratula": self.caratula,
            "horas": self.horas,
            "logros": self.logros or [],
            "plataforma": self.plataforma
        }
    @classmethod
    def from_dict(cls, data: dict)-> "Juego":
        fecha_str = data.get("fecha")
        fecha = datetime.fromisoformat(fecha_str) if fecha_str else None
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre", ""),
            genero=data.get("genero", ""),
            fecha=fecha,
            descripcion=data.get("descripcion", ""),
            caratula=data.get("caratula"),
            horas=data.get("horas", 0.0),
            logros=data.get("logros") or [],
            plataforma=data.get("plataforma")
        )