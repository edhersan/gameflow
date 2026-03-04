import requests

class APIClient:
    BASE_URL = "http://127.0.0.1:8000"

    def obtener_juegos(self):
        r= requests.get(f"{self.BASE_URL}/juegos")
        r.raise_for_status()
        return r.json()
    
    def agregar_juego(self, juego):
        r = requests.post(f"{self.BASE_URL}/juegos", json=juego)
        r.raise_for_status()
        return r.json()
    
    def actualizar_juego(self, id_juego: int, data: dict):
        r = requests.put(f"{self.BASE_URL}/juegos/{id_juego}", json=data)
        r.raise_for_status()
        return r.json()
    
    def eliminar_juego(self, id_juego: int):
        r = requests.delete(f"{self.BASE_URL}/juegos/{id_juego}")
        r.raise_for_status()
        return r.json()
    
    def descargar_caratula(self, id_juego: int):
        r = requests.post(f"{self.BASE_URL}/juegos/{id_juego}/caratula/auto")
        r.raise_for_status()
        return r.json()