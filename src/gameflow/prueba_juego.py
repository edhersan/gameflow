from modelo import Juego
from datetime import date

j1 = Juego(
    nombre="The Witcher 3",
    genero="RPG",
    fecha=date(2015, 5, 19),
    descripcion="Un RPG brutal.",
    horas=120
)

print(j1)
print(j1.nombre)
print(j1.fecha)