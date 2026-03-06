🎮 GameFlow — Tu Biblioteca de Juegos Personal
GameFlow es una aplicación de escritorio desarrollada en Python, que combina una interfaz gráfica moderna con Tkinter, un backend con FastAPI, y una base de datos SQLite para gestionar y visualizar tu biblioteca de juegos.
Incluye funciones como:

CRUD completo (agregar, modificar, eliminar)
Descarga automática de carátulas desde RAWG API
Vista en lista con búsqueda
Panel de detalles con carátula + información del juego
Ventanas secundarias para edición
Gestión local de carátulas y almacenamiento persistente

GameFlow fue desarrollado como proyecto personal para portafolio.

🚀 Tecnologías usadas
Frontend / GUI

Python 3
Tkinter
Pillow (PIL)
ttk (Treeview styling)

Backend

FastAPI
SQLite3
requests
RAWG API (para obtener carátulas reales)


🧭 Características principales
✔ 1. Interfaz gráfica completa

Menú superior con opciones CRUD
Barra de búsqueda en tiempo real
Panel izquierdo con lista de juegos
Panel derecho con la información completa del juego seleccionado

✔ 2. CRUD completo

Agregar juego: formulario dedicado
Modificar juego: edita sin perder valores existentes
Borrar juego: confirmación + actualización inmediata

✔ 3. Descarga automática de carátulas
GameFlow permite obtener carátulas mediante RAWG API:

Busca por nombre del juego
Descarga la imagen real
Guarda la carátula en:
~/.gameflow/caratulas/
Actualiza la información del juego en la base de datos

✔ 4. Almacenamiento persistente
Base de datos SQLite con tabla juegos, que almacena:

nombre
género
descripción
fecha
plataforma
horas jugadas
logros
ruta de la carátula

✔ 5. Vista limpia y organizada

Lista de juegos ordenada y oscura (tipo launcher)
Panel derecho estilo dashboard


✨ Posibles mejoras futuras
Algunas ideas para expandir GameFlow:

Integración con plataformas reales (Steam, Epic, GOG) para:
obtener horas jugadas automáticamente
importar logros
sincronizar biblioteca

Miniaturas en el Treeview
Tema oscuro avanzado con ttkbootstrap
Exportar la biblioteca como HTML
Generar estadísticas de hábitos de juego
Modo ventana/tema personalizable
Animaciones y transiciones para UI (solo si se cambia de framework)


🛠️ Instalación y ejecución
1. Clonar repositorio
Pythongit clone https://github.com/edhersan/gameflow.gitcd gameflowMostrar más líneas
2. Instalar dependencias
Shellpip install -r requirements.txtMostrar más líneas
3. Iniciar backend
Shellcd backenduvicorn api:app --reload --port 8000Mostrar más líneas
4. Iniciar GUI
Shellcd srcpython3 -m gameflow.mainMostrar más líneas

📂 Estructura del proyecto
gameflow/
│
├── backend/
│   ├── api.py
│   ├── config.py
│   ├── ...
│
├── assets/
│   └── (futuros iconos, fondos o recursos)
│
├── src/
│   └── gameflow/
│       ├── main.py
│       ├── biblioteca.py
│       ├── modelo.py
│       ├── api_client.py
│       ├── gui/
│       │   └── ventana_principal.py
│
└── README.md


🧑‍💻 Autor
Proyecto desarrollado por Eduwin Sánchez
Parte de su portafolio para ingeniería de software y desarrollo Python.
