from typing import List, Optional
from .modelo import Juego

class Biblioteca:
    def __init__(self):
        self.juegos: List[Juego] = []

    def obtener_por_id(self, id_juego: int) -> Optional[Juego]:
        for juego in self.juegos:
            if juego.id == id_juego:
                return juego
        return None

    
    def existe(self, nombre: str, plataforma: str = None) -> bool:
        nombre = (nombre or "").strip().lower()
        plataforma = (plataforma or "").strip().lower()

        for j in self.juegos:
            j_nombre = (j.nombre or "").strip().lower()
            j_plataforma = (j.plataforma or "").strip().lower()

            if j_nombre == nombre and j_plataforma == plataforma:
                return True

        return False


    def agregar(self, juego: Juego)-> bool:

        nombre = (juego.nombre or "").strip().lower()
        plataforma = (juego.plataforma or "").strip().lower()

        for j in self.juegos:
            j_nombre = (j.nombre or "").strip().lower()
            j_plataforma = (j.plataforma or "").strip().lower()

            if j_nombre == nombre and j_plataforma == plataforma:
                return False  # no se agrega
       
        self.juegos.append(juego)
        return True

    def agregar_juego(self, juego: Juego):
        """Alias para agregar()"""
        self.agregar(juego)

    def obtener_todos(self) -> List[Juego]:
        """Retorna todos los juegos de la biblioteca."""
        return self.juegos
    
    def listar_juegos(self) -> List[Juego]:
        """Alias para obtener_todos()"""
        return self.obtener_todos()
    
    def buscar(self, nombre: str = "", genero: str = "", plataforma: str = ""):
        nombre = (nombre or "").strip().lower()
        genero = (genero or "").strip().lower()
        plataforma = (plataforma or "").strip().lower()

        resultados = []

        for j in self.juegos:
            j_nombre = (j.nombre or "").strip().lower()
            j_genero = (j.genero or "").strip().lower()
            j_plataforma = (j.plataforma or "").strip().lower() 

            if nombre and nombre not in j_nombre:
                continue
            if genero and genero != j_genero:
                continue
            if plataforma and plataforma != j_plataforma:
                continue
        resultados.append(j)

        return resultados
    
    def eliminar(self, juego: Juego) -> bool:
        if juego.id is not None:
            for j in self.juegos:
                if j.id == juego.id:
                    self._juegos.remove(j)
                    return True
        return False
        if juego in self.juegos:
            self._juegos.remove(juego)
            return True 
        return False
    
    def eliminar_por_id(self, id_juego: int) -> bool:
        for j in self.juegos:
            if j.id == id_juego:
                self.juegos.remove(j)
                return True
        return False
    
    def actualizar(self, juego: Juego)-> bool:
        if juego.id is None:
            return False
        
        for indice, actual in enumerate(self.juegos):
            if actual.id == juego.id:
                self.juegos[indice] = juego
                return True
        return False
    
    def ordenar_por(self, atributo: str, descendente: bool = False)-> None:
        try:
            self.juegos.sort(key=lambda j: getattr(j, atributo), reverse=descendente)
        except Exception:
            pass

    def obtener_por_id(self, id_juego: int) -> Optional[Juego]:
        for juego in self.juegos:
            if juego.id == id_juego:
                return juego
        return None

    