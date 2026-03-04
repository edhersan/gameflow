import tkinter as tk
from datetime import date

from gameflow.biblioteca import Biblioteca
from gameflow.modelo import Juego
from .api_client import APIClient
from PIL import Image, ImageTk
import io


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.api = APIClient()
        self.juegos=[]
        self.biblioteca = Biblioteca()         # Aquí creamos la biblioteca
        self._configurar_ventana()             # Configurar ventana base
        self._cargar_juegos_desde_api()
        self.lista_juegos.bind("<<ListboxSelect>>", self.on_juego_seleccionado)

    def _configurar_ventana(self):
        """Configura la ventana principal (tamaño, título, etc.)."""
        self.root.title("GAMeFLOw")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")
        #frame izquierdo
        self.frame_izquierdo = tk.Frame(self.root, bg="#2b2b2b", width=250)
        self.frame_izquierdo.pack(side="left", fill="y")
        #un scrollbar para la lista de juegos
        self.scroll=tk.Scrollbar(self.frame_izquierdo)
        self.scroll.pack(side="right", fill="y")
        #el listbox para mostrar los juegos
        self.lista_juegos=tk.Listbox(self.frame_izquierdo, 
                                     bg="gray20", 
                                     fg="white", 
                                     font=("Consolas", 11), 
                                     yscrollcommand=self.scroll.set)
        
        self.lista_juegos.pack(fill="both", expand=True, padx=5, pady=5)
        self.lista_juegos.config(width=0)
        self.scroll.config(command=self.lista_juegos.yview)
        #frame derecho
        self.frame_derecho = tk.Frame(self.root, bg="#1e1e1e")

        self.frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        #contenedor central
        self.frame_central = tk.Frame(self.frame_derecho, bg="#1e1e1e")
        self.frame_central.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        #label caratula
        self.label_caratula = tk.Label(self.frame_central, bg="#1e1e1e")
        self.label_caratula.pack(pady=10)
        #label de titulo
        self.label_titulo = tk.Label(self.frame_central, bg="#1e1e1e", fg="white", font=("Consolas", 16, "bold"))
        self.label_titulo.pack(anchor="w", pady=5)
        #label de genero/plataforma
        self.label_info = tk.Label(self.frame_central, bg="#1e1e1e", fg="white", font=("Consolas", 12))
        self.label_info.pack(anchor="w", pady=5)
        #label de descripcion
        self.label_descripcion = tk.Label(self.frame_central, bg="#1e1e1e", fg="white", font=("Consolas", 11), wraplength=600, )
        self.label_descripcion.pack(anchor="w", pady=10)

   
    def _cargar_juegos_desde_api(self):
        try:
            juegos_json = self.api.obtener_juegos()
            self.juegos = juegos_json

            self.lista_juegos.delete(0, tk.END)
            for j in self.juegos:
                self.lista_juegos.insert(tk.END, f"{j['id']}: {j['nombre']} ({j['plataforma']})  ")
                print("Juego cargado desde API a la ventana")
        except Exception as e:
            print(f"Error al cargar juegos desde la API: {e}")

    def on_juego_seleccionado(self, event):
        seleccion = self.lista_juegos.curselection()
        if not seleccion:
            return  # No hay selección, salir sin hacer nada

        # Obtener el índice del juego seleccionado
        indice = seleccion[0]
        juego_seleccionado = self.juegos[indice]
        #mostrar detallles y la caratula
        print("selecionaste:", juego_seleccionado['nombre'])

    def on_juego_seleccionado(self, event):
        seleccion = self.lista_juegos.curselection()
        if not seleccion:
            return  # No hay selección, salir sin hacer nada

        # Obtener el índice del juego seleccionado
        indice = seleccion[0]
        juego_seleccionado = self.juegos[indice]
        #mostrar detallles y la caratula
        print("selecionaste:", juego_seleccionado['nombre'])
        self.label_titulo.config(text=juego_seleccionado['nombre'])
        self.label_info.config(text=f"{juego_seleccionado['genero']} - {juego_seleccionado['plataforma']}")
        self.label_descripcion.config(text=juego_seleccionado['descripcion'])

        ruta_caratula = juego_seleccionado.get("caratula")
        if ruta_caratula:
            try:
                img = Image.open(ruta_caratula)
                img = img.resize((450, 350))

                self.tk_img_caratula = ImageTk.PhotoImage(img)
                self.label_caratula.config(image=self.tk_img_caratula)
            except Exception as e:
                print(f"Error al cargar la imagen de la carátula: {e}")

                self.label_caratula.config(image="", text="No se pudo cargar la carátula", fg="white", font=("Consolas", 12))
        else:
            self.label_caratula.config(image="", text="No hay carátula disponible", fg="white", font=("Consolas", 12))


            
           
    