import tkinter as tk
import io
import os

from datetime import date
from gameflow.biblioteca import Biblioteca
from gameflow.modelo import Juego
from .api_client import APIClient
from PIL import Image, ImageTk
from tkinter import ttk



class VentanaPrincipal:

    def _ruta(self, path_relativo: str) -> str:
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base, path_relativo)


    def __init__(self, root):
        self.root = root
        self.root.title ("GameFlow")
        self.root.geometry("1250x650")
        self.api=APIClient()
        self.juegos=[]
        self.juegos_por_id={}
        self._crear_menubar()
        self._crear_barra_superior()

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
        "Treeview",
        background="#2b2b2b",
        foreground="white",
        rowheight=28,
        fieldbackground="#2b2b2b",
        bordercolor="#2b2b2b",
        borderwidth=0
        )

        style.map(
        "Treeview",
        background=[("selected", "#404040")]
        )


        #panel izquierdo donde va el treeview
        self.frame_izquierdo= tk.Frame(self.root, bg="#2b2b2b", width=280)
        self.frame_izquierdo.pack(side="left", fill="y")
        #scrollbar del panel izquierdo
        self.scroll_y=tk.Scrollbar(self.frame_izquierdo, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")
        #treeview
        self.tree= ttk.Treeview(self.frame_izquierdo, columns=("plataforma",), show="tree headings",
        yscrollcommand=self.scroll_y.set, height=20
        )
        #encabezados
        self.tree.heading("#0", text="juego")
        self.tree.heading("plataforma", text="plataforma")
        #ancho de columnas
        self.tree.column("#0", width=200, anchor="w")
        self.tree.column("plataforma", width=80, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.scroll_y.config(command=self.tree.yview)
        #seleccion de juego
        self.tree.bind("<<TreeviewSelect>>", self._on_juego_seleccionado)
        #fondo 
        
        self.frame_derecho = tk.Frame(self.root, bg="#1e1e1e")
        self.frame_derecho.pack(side="left", fill="both", expand=True)
        self._crear_panel_derecho()

        self._cargar_juegos_desde_api()

    #creamos la barra de menu
    def _crear_menubar(self):
        menubar = tk.Menu(self.root)

        #menu opciones
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="agregar juego", command=self._abrir_ventana_agregar)
        menu_archivo.add_command(label="modificar juego", command=self._abrir_ventana_modificar)
        menu_archivo.add_command(label="borrar juego", command=self._abrir_ventana_borrar)
        menu_archivo.add_command(label="obtener caratula", command=self._obtener_caratula_desde_gui)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Cerrar", command=self.root.quit)

        menubar.add_cascade(label="opciones", menu=menu_archivo)

        #menu acerca de
        menu_acerca=tk.Menu(menubar, tearoff=0)
        menu_acerca.add_command(label="acerca de", command=self._mostrar_acerca_de)
        menubar.add_cascade(label="acerca de", menu=menu_acerca)

        self.root.config(menu=menubar)

    def _abrir_ventana_agregar(self):
            win=tk.Toplevel(self.root)
            win.title("Agregar Juego")
            win.configure(bg="#1e1e1e")
            win.geometry("400x500")
            win.resizable(False,False)
            #campos
            fuente=("Consolas", 11)
            #nombre
            tk.Label(win, text="Nombre", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            entry_nombre=tk.Entry(win, width=40)
            entry_nombre.pack(padx=20)
            #genero
            tk.Label(win, text="genero", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            entry_genero=tk.Entry(win, width=40)
            entry_genero.pack(padx=20)
            #plataforma
            tk.Label(win, text="Plataforma", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            entry_plataforma=tk.Entry(win, width=40)
            entry_plataforma.pack(padx=20)
            #fecha
            tk.Label(win, text="Fecha (AA-MM-DD)", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            entry_fecha=tk.Entry(win, width=40)
            entry_fecha.pack(padx=20)
            #descripcion
            tk.Label(win, text="Descripcion", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            txt_descripcion=tk.Text(win, width=40, height=6)
            txt_descripcion.pack(padx=20)
            #botones
            frame_botones = tk.Frame(win, bg="#1e1e1e")
            frame_botones.pack(pady=20)

            def guardar_juego():
                data = {
                    "nombre": entry_nombre.get().strip(),
                    "genero": entry_genero.get().strip(),
                    "fecha": entry_fecha.get().strip(),
                    "descripcion": txt_descripcion.get("1.0", tk.END).strip(),
                    "caratula": None,
                    "horas": 0,
                    "logros": None,
                    "plataforma": entry_plataforma.get().strip()
                }
                try:
                    self.api.agregar_juego(data)
                    self._cargar_juegos_desde_api()
                    win.destroy()
                except Exception as e:
                    print("Error agregando juego", e)
             
            btn_guardar= tk.Button(frame_botones, text="Guardar", bg="#3c3c3c", fg="white", width=10, command=guardar_juego)
            btn_guardar.pack(side="left", padx=10)
            btn_cancelar= tk.Button(frame_botones, text="cancelar", bg="#3c3c3c", fg="white", width=10, command=win.destroy)
            btn_cancelar.pack(side="left", padx=10)

            win.transient(self.root)
            win.grab_set()



    def _abrir_ventana_modificar(self):
            #verificar que el juego si esta
            seleccion=self.tree.selection() 
            if not seleccion:
                  print("no hay juego para modificar")
                  return
            item_id= seleccion[0]
            juego_id= int(item_id)
            juego= self.juegos_por_id.get(juego_id)
            if not juego:
                  print("No se encontro el juego en la biblioteca")
                  return
            #aca la ventana
            win=tk.Toplevel(self.root)
            win.title("Actualizar Juego")
            win.configure(bg="#1e1e1e")
            win.geometry("400x500")
            win.resizable(False,False)
            #campos
            fuente=("Consolas", 11)
            #nombre
            tk.Label(win, text="Nombre", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            entry_nombre=tk.Entry(win, width=40)
            entry_nombre.pack(padx=20)
            #genero
            tk.Label(win, text="genero", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            entry_genero=tk.Entry(win, width=40)
            entry_genero.pack(padx=20)
            #plataforma
            tk.Label(win, text="Plataforma", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            entry_plataforma=tk.Entry(win, width=40)
            entry_plataforma.pack(padx=20)
            #fecha
            tk.Label(win, text="Fecha (AA-MM-DD)", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            entry_fecha=tk.Entry(win, width=40)
            entry_fecha.pack(padx=20)
            #descripcion
            tk.Label(win, text="Descripcion", fg="white", bg="#1e1e1e", font=fuente).pack(anchor="w", padx=20, pady=(15, 0))
            txt_descripcion=tk.Text(win, width=40, height=6)
            txt_descripcion.pack(padx=20)
    
            def actualizar_juego():

                nombre_nuevo = entry_nombre.get().strip()
                genero_nuevo = entry_genero.get().strip()
                plataforma_nueva = entry_plataforma.get().strip()
                fecha_nueva = entry_fecha.get().strip()
                descripcion_nueva = txt_descripcion.get("1.0", tk.END).strip()

               
                data = {
                        "nombre": nombre_nuevo or juego.get("nombre", ""),
                        "genero": genero_nuevo or juego.get("genero", ""),
                        "fecha": fecha_nueva or juego.get("fecha", ""),
                        "descripcion": descripcion_nueva or juego.get("descripcion", ""),
                        "caratula": juego.get("caratula"),
                        "horas": juego.get("horas", 0),
                        "logros": juego.get("logros"),
                        "plataforma": plataforma_nueva or juego.get("plataforma", "")
                        }

                try:
                    self.api.actualizar_juego(juego_id, data)
                    self._cargar_juegos_desde_api()
                    win.destroy()
                except Exception as e:
                    print("Error actualizando juego", e)

            frame_botones = tk.Frame(win, bg="#1e1e1e")
            frame_botones.pack(pady=20)
             
            btn_guardar= tk.Button(frame_botones, text="Guardar", bg="#3c3c3c", fg="white", width=10, command=actualizar_juego)
            btn_guardar.pack(side="left", padx=10)
            btn_cancelar= tk.Button(frame_botones, text="cancelar", bg="#3c3c3c", fg="white", width=10, command=win.destroy)
            btn_cancelar.pack(side="left", padx=10)

            win.transient(self.root)
            win.grab_set()

    def _obtener_caratula_desde_gui(self):
        seleccion = self.tree.selection()
        if not seleccion:
                print("No hay juego seleccionado para obtener carátula")
                return
        item_id=seleccion[0]
        juego_id= int(item_id)
        try:
             print(f"obteniendo caratula para EL JUEGO {juego_id}")
             self.api.descargar_caratula(juego_id)
             self._cargar_juegos_desde_api()
             self.tree.selection_set(str(juego_id))
             self.tree.focus(str(juego_id))
             self._on_juego_seleccionado(None)
             print("descarga correcta")
        except Exception as e:
             print("no se pudo obtener la caratula", e)
 
        

    def _abrir_ventana_borrar(self):
        # Verificar selección
        seleccion = self.tree.selection()
        if not seleccion:
                print("No hay juego seleccionado para borrar")
                return

        item_id = seleccion[0]
        juego_id = int(item_id)
        juego = self.juegos_por_id.get(juego_id)

        if not juego:
                print("Juego no encontrado en juegos_por_id")
                return

        # Crear ventana de confirmación
        win = tk.Toplevel(self.root)
        win.title("Borrar juego")
        win.configure(bg="#1e1e1e")
        win.geometry("350x180")
        win.resizable(False, False)

        mensaje = f"¿Seguro que quieres borrar:\n\n     {juego.get('nombre', '')}?"

        lbl = tk.Label(
                win,
                text=mensaje,
                bg="#1e1e1e",
                fg="white",
                font=("Consolas", 11),
                justify="center"
                )
        lbl.pack(padx=20, pady=(20, 10))

        frame_botones = tk.Frame(win, bg="#1e1e1e")
        frame_botones.pack(pady=10)

        def borrar():
            try:
                self.api.eliminar_juego(juego_id)  # DELETE /juegos/{id}
                self._cargar_juegos_desde_api()
                # Limpiar panel derecho si era ese el seleccionado
                self.label_titulo.config(text="")
                self.label_plataforma.config(text="")
                self.label_anio.config(text="")
                self.label_horas.config(text="")
                self.label_descripcion.config(text="")
                self.label_logros.config(text="")
                self.label_caratula.config(image="", text="")
                win.destroy()
            except Exception as e:
                print("Error borrando juego:", e)

        btn_borrar = tk.Button(frame_botones, text="Borrar", bg="#a00000", fg="white", width=10, command=borrar)
        btn_borrar.pack(side="left", padx=10)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar", bg="#3c3c3c", fg="white", width=10, command=win.destroy)
        btn_cancelar.pack(side="left", padx=10)

        win.transient(self.root)
        win.grab_set()

            
        
        
    def _mostrar_acerca_de(self):
            win=tk.Toplevel(self.root)
            win.title("acerca de gameflow")
            win.configure(bg="black")
            win.geometry("420x300")
            win.resizable(False,False)

            lbl_titulo=tk.Label(
                  win,
                  text="GameFlow",
                  font=("Consolas", 18, "bold"),
                  fg="white",
                  bg="#1e1e1e"
                  )
            lbl_titulo.pack(pady=(20, 10))
            descripcion=(

                    "Aplicación desarrollada por Eduwin Sánchez como parte\n"
                    "de su portafolio profesional.\n\n"
                    "Versión: 1.0\n"
                    "Backend: FastAPI + SQLite\n"
                    "Frontend: Tkinter\n"
                    "API externa: RAWG.io"
                    )
            lbl_texto=tk.Label(
                  win,
                  text=descripcion,
                  font=("Consolas", 12),
                  fg="white",
                  bg="#1e1e1e",
                  justify="center",
                  wraplength=380,
                  anchor="center"
            )
            lbl_texto.pack(pady=10, padx=20, fill="both", expand=True)

            btn_cerrar=tk.Button(
                  win,
                  text="cerrar",
                  command=win.destroy,
                  bg="#3c3c3c",
                  fg="white",
                  width=12
            )
            btn_cerrar.pack(pady=10)
            win.transient(self.root)
            win.grab_set()

        #barra superior/barra de busqueda
    def _crear_barra_superior(self):
        self.barra_superior = tk.Frame(self.root, bg="#2b2b2b", height=32)
        self.barra_superior.pack(side="top", fill="x")
        #boton lupa
        self.btn_buscar=tk.Button(
              self.barra_superior,
              text="🔍",
              bg="#3c3c3c",
              fg="white",
              relief="flat",
        command=self._buscar_desde_gui

        )
        self.btn_buscar.pack(side="right", padx=(5,10), pady=4)
        #entrada de texto
        self.entry_buscar=tk.Entry(self.barra_superior)
        self.entry_buscar.pack(side="right", padx=(0,5), pady=4)
        self.entry_buscar.bind("<Return>", self._buscar_desde_gui)
        #label buscar
        lbl_buscar= tk.Label(
              self.barra_superior,
              text="Buscar",
              bg="#2b2b2b",
              fg="white"
        )
        lbl_buscar.pack(side="right", padx=(0,5), pady=4)
    #funcion busqueda
    def _buscar_desde_gui(self, event=None):
        texto=self.entry_buscar.get().strip().lower()
        #limpiar treeview
        for item in self.tree.get_children():
              self.tree.delete(item)
        #sin texto mostrarlos todos
        if not texto:
              juegos_filtrados = self.juegos
        else:      
                juegos_filtrados=[
                    j for j in self.juegos
                    if texto in j["nombre"].lower() or texto in (j.get("plataforma") or "").lower()
              ] 
        #volver a cargar el treeview
        self._llenar_treeview(juegos_filtrados)
        #borrar texto
        self.entry_buscar.delete(0,tk.END) 

    #treeview helpers
    def _llenar_treeview(self, lista_juegos):
        # Opcional: mapa por id para acceso rápido
        self.juegos_por_id = {j["id"]: j for j in lista_juegos}

        # Limpiar Treeview
        for item in self.tree.get_children():
                self.tree.delete(item)

        # Insertar filas
        for j in lista_juegos:
                juego_id = j["id"]
                nombre = j["nombre"]
                plataforma = j.get("plataforma") or ""

                self.tree.insert(
                "", "end",
                iid=str(juego_id),       # usamos id como identificador
                text=nombre,             # texto en la columna principal
                values=(plataforma,)     # columna "plataforma"
        )

    def _cargar_juegos_desde_api(self):
        try:
                juegos_json = self.api.obtener_juegos()
                self.juegos = juegos_json  # guardamos la lista completa

        # Llenar el Treeview con todos los juegos al inicio
                self._llenar_treeview(self.juegos)

                print("Juegos cargados desde API en el Treeview")
        except Exception as e:
                print("Error al cargar desde la API:", e)


    def _crear_panel_derecho(self):
          #el frame superior que va en 2 partes por la caratula y eso
          frame_sup= tk.Frame(self.frame_derecho, bg="#1e1e1e")
          frame_sup.pack(fill="x", padx=20, pady=(20,10))
          #la caratula
          self.label_caratula= tk.Label(frame_sup, bg="#1e1e1e", width=280, height=400)
          self.label_caratula.pack_propagate(False)
          self.label_caratula.pack(side="left", padx=(0, 20))
          #los textos(titulo,plataforma,year,horas)
          frame_texto = tk.Frame(frame_sup, bg="#1e1e1e")
          frame_texto.pack(side="left", fill="x", expand=True)
          
          self.label_titulo= tk.Label(
                frame_texto,
                text="",
                bg="#1e1e1e",
                fg="white",
                font=("Consolas", 24, "bold"),
                anchor="w"
          )
          self.label_titulo.pack(fill="x", pady=(0, 5))

          self.label_plataforma= tk.Label(
                frame_texto,
                text="",
                bg="#1e1e1e",
                fg="white",
                font=("Consolas", 12),
                anchor="w"
          )
          self.label_plataforma.pack(fill="x", pady=(0, 5))

          self.label_anio= tk.Label(
                frame_texto,
                text="",
                bg="#1e1e1e",
                fg="white",
                font=("Consolas", 12),
                anchor="w"
          )
          self.label_anio.pack(fill="x", pady=(0, 5))

          self.label_horas= tk.Label(
                frame_texto,
                text="",
                bg="#1e1e1e",
                fg="white",
                font=("Consolas", 12),
                anchor="w"
          )
          self.label_horas.pack(fill="x", pady=(0, 5))
          #descripcion
          self.label_descripcion= tk.Label(
                frame_texto,
                text="",
                bg="#1e1e1e",
                fg="white",
                font=("Consolas", 12),
                justify="left",
                wraplength=600,
                anchor="nw"
          )
          self.label_descripcion.pack(fill="both", padx=20, pady=(0, 10))
          #logros centradito abajo
          
          self.label_logros_titulo = tk.Label(
                self.frame_derecho,
                text="Logros",
                bg="#1e1e1e",
                fg="white",
                font=("Consolas", 12, "bold")
        )
          self.label_logros_titulo.pack(pady=(40, 0))

          self.label_logros = tk.Label(
                self.frame_derecho,
                text="",
                bg="#1e1e1e",
                fg="white",
                font=("Consolas", 11),
                justify="center"
        )
          self.label_logros.pack(pady=(5, 40))


    def _on_juego_seleccionado(self, event):
          seleccion= self.tree.selection() 
          if not seleccion: 
                return
          item_id=seleccion[0]
          juego_id= int(item_id)

          juego= self.juegos_por_id.get(juego_id)
          if not juego:
                return
          #texto
          titulo= juego.get("nombre", "")
          plataforma= juego.get("plataforma") or ""
          fecha= juego.get("fecha") or ""
          anio= fecha.split("-")[0] if fecha else ""
          horas=juego.get("horas", 0)
          descripcion= juego.get("descripcion") or ""
          logros= juego.get("logros") or ""

          self.label_titulo.config(text=titulo)
          self.label_plataforma.config(text=f"plataforma: {plataforma}")
          self.label_anio.config(text=f"Año: {anio}")
          self.label_horas.config(text=f"horas jugadas: {horas}")
          self.label_descripcion.config(text=descripcion)
          self.label_logros.config(text=logros)

          ruta_caratula=(juego.get("caratula") or "").strip()            
          print("ruta caratula", ruta_caratula, repr(ruta_caratula), "exists:",os.path.exists(ruta_caratula))
          if ruta_caratula and os.path.exists(ruta_caratula):
           try:
                img=Image.open(ruta_caratula)
                img=img.resize((280, 400))
                self._img_caratula= ImageTk.PhotoImage(img)
                self.label_caratula.config(image=self._img_caratula, text="")
           except Exception as e:
                    print("error al cargar la caratula", e)
                    self.label_caratula.config(image="", text="sin caratula")
          else:
                self.label_caratula.config(image="", text="no hay caratula")

                


def main():
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":    
    main()

   