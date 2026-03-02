from datetime import date
from modelo import Juego
from biblioteca import Biblioteca

bib = Biblioteca()

j1 = Juego(
    nombre="Hollow Knight",
    genero="Metroidvania",
    fecha=date(2017, 2, 24),
    descripcion="Mi favorito."
)

j2 = Juego(
    nombre="Celeste",
    genero="Plataformas",
    fecha=date(2018, 1, 25),
    descripcion="Desafiante y hermoso."
)

bib.agregar_juego(j1)
bib.agregar_juego(j2)

print("Todos los juegos:")
for j in bib.listar_juegos():
    print(" -", j.nombre)

print("\nBuscar 'hollow':")
for j in bib.buscar_por_nombre("hollow"):
    print(" ->", j.nombre)

bib.eliminar(j1)

print("\nDespués de eliminar Hollow Knight:")
for j in bib.listar_juegos():
    print(" -", j.nombre)