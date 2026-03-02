from datetime import date
from modelo import Juego
from biblioteca import Biblioteca

bib = Biblioteca()

j1 = Juego(nombre="Portal 2", genero="Puzzle", fecha=..., descripcion="...")
j2 = Juego(nombre="Portal 2", genero="Puzzle", fecha=..., descripcion="...")

print(bib.agregar(j1))  # True
print(bib.agregar(j2))  # False
