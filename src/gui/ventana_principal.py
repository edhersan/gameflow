import tkinter as tk
from datetime import date

from gameflow.biblioteca import Biblioteca
from gameflow.modelo import Juego


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.biblioteca = Biblioteca()         # Aquí creamos la biblioteca
        self._configurar_ventana()             # Configurar ventana base
        self._cargar_juegos_de_prueba()        # Cargar juegos de ejemplo
        self._mostrar_juegos()                 # Ponerlos en pantalla

    def _configurar_ventana(self):
        """Configura la ventana principal (tamaño, título, etc.)."""
        self.root.geometry("800x600")
        self.root.configure(bg="#222222")

        # Creamos un frame donde más adelante irán la lista/panel
        self.frame_lista = tk.Frame(self.root, bg="#222222")
        self.frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    def _cargar_juegos_de_prueba(self):
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

        self.biblioteca.agregar(j1)
        self.biblioteca.agregar(j2)

    def _mostrar_juegos(self):
        juegos = self.biblioteca.obtener_todos()

        # Limpiar el frame por si se vuelve a llamar
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        for juego in juegos:
            lbl = tk.Label(
                self.frame_lista,
                text=juego.nombre,
                fg="white",
                bg="#222222",
                anchor="w"
            )
            lbl.pack(fill="x", padx=5, pady=3)
            lbl = tk.Label(
                self.frame_lista,
                text=juego.descripcion,
                fg="white",
                bg="#222222",
                anchor="w"
            )
            lbl.pack(fill="x", padx=5, pady=3)
             
            lbl = tk.Label(
                self.frame_lista,
                text=juego.genero,
                fg="white",
                bg="#222222",
                anchor="w"
            )
            lbl.pack(fill="x", padx=5, pady=3)

            lbl = tk.Label(
                self.frame_lista,
                text=juego.fecha.strftime("%Y-%m-%d"),
                fg="white",
                bg="#222222",
                anchor="w"
            )
            lbl.pack(fill="x", padx=5, pady=3)