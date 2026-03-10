# 🎮 GameFlow — Tu Biblioteca de Juegos Personal

**GameFlow** es una aplicación de escritorio hecha en Python que te permite administrar tu biblioteca de videojuegos con una interfaz moderna, oscura y pensada para ser simple y útil.
Incluye desde un CRUD completo hasta descarga automática de carátulas gracias a la API de RAWG.

---

## 🚀 Tecnologías Utilizadas

* **Frontend:** Python 3, Tkinter, Pillow (PIL), ttk.
* **Backend:** FastAPI, SQLite3, Requests.
* **API Externa:** RAWG API (Metadatos y carátulas).

---

## 🧭 Características Principales

* **Interfaz Completa:** Menú funcional, búsqueda en tiempo real y panel de detalles.
* **Gestión CRUD:** Control total sobre la edición y eliminación de títulos.
* **Automatización:** Descarga de arte oficial directo a tu almacenamiento local.
* **Persistencia:** Base de datos robusta para horas de juego, logros y plataformas.

---

## 🛠️ Instalación y Ejecución

### 🪟 Windows
1. Descarga el instalador en Releases.
2. Ejecuta el archivo e instálalo en tu sistema.

### 🐧 Debian / Ubuntu
Descarga el instalador en Releases.
Para instalar el paquete .deb, utiliza los comandos:
**sudo dpkg -i gameflow.deb**
**sudo apt --fix-broken install**

### 💻 Modo Desarrollador (Código Fuente)
Para correr el proyecto manualmente, sigue estos pasos en tu terminal:

1. **Clonar e instalar:** git clone https://github.com/edhersan/gameflow.git && pip install -r requirements.txt
2. **Backend:** cd backend && uvicorn api:app --port 8000
3. **Frontend:** cd src && python3 -m gameflow.main

---

## 📂 Estructura del Proyecto

* **backend/**: Lógica de la API y gestión de base de datos.
* **assets/**: Iconos y recursos estáticos del sistema.
* **src/gameflow/**: Código fuente, módulos de GUI y cliente de API.

---

## 📸 Capturas de Pantalla

| | |
| :---: | :---: |
| ![GameFlow](./screenshots/Captura%20de%20pantalla%202026-03-08%20162606.png) | ![GameFlow](./screenshots/Captura%20de%20pantalla%202026-03-08%20162848.jpg) |
| ![GameFlow](./screenshots/Captura%20de%20pantalla%202026-03-08%20162946.jpg) | ![GameFlow](./screenshots/Captura%20de%20pantalla%202026-03-08%20163209.jpg) |
| ![GameFlow](./screenshots/Captura%20de%20pantalla%202026-03-10%20155237.jpg) | ![GameFlow](./screenshots/Captura%20de%20pantalla_20260310_160939.png) |
| ![GameFlow](./screenshots/Captura%20de%20pantalla_20260310_161050.png) | |


---

## ✨ Mejoras Futuras

* Integración con Steam, Epic y GOG.
* Modo oscuro avanzado con ttkbootstrap.
* Estadísticas avanzadas de juego y exportación a HTML.

---

## 🧑‍💻 Autor
**Edwin Sánchez**
*Estudiante de Ingeniería de Software*
[Visitar Perfil de GitHub](https://github.com/edhersan)
