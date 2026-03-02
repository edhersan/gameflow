from typing import List
from gameflow.modelo import Juego

class Biblioteca:
    def __init__(self):
        self.juegos: List[Juego] = []

    def agregar_juego(self, juego: Juego):
        self.juegos.append(juego)

    def agregar(self, juego: Juego):
        """Alias para agregar_juego()"""
        self.agregar_juego(juego)

    def listar_juegos(self) -> List[Juego]:
        return self.juegos
    
    def obtener_todos(self) -> List[Juego]:
        """Alias para listar_juegos()"""
        return self.listar_juegos()
    
    def buscar_por_nombre(self, texto: str) -> list[Juego]:
        return [j for j in self.juegos if texto.lower() in j.nombre.lower()]
    
    def eliminar(self, juego: Juego):
        if juego in self.juegos:
            self.juegos.remove(juego)

    