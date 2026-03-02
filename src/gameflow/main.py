import tkinter as tk
from gui.ventana_principal import VentanaPrincipal

def main():
    root = tk.Tk()
    root.title("GameFlow")
    
    app = VentanaPrincipal(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
