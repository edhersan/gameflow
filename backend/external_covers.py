import requests
import urllib.parse
import os

RAW_API_KEY = "AQUI_VA_TU_API_KEY_DE_RAWG"  # Reemplaza esto con tu propia API key de RAWG
RAW_ENDPOINT = "https://api.rawg.io/api/games"


def buscar_caratula_por_titulo(titulo: str) -> str|None:
    # Utiliza la API de Google Custom Search para buscar la carátula del juego por su título
    if not titulo:
        return None
    
    params = {
        "search": titulo,
        "key": RAW_API_KEY,
    }

    response = requests.get(RAW_ENDPOINT, params=params)

    if response.status_code != 200:
        return None
    
    data = response.json()
#validar que haya resultados
    if "results" in data and len(data["results"]) == 0:
        return None
    
    #primer resultado, mejor resultado
    juego = data["results"][0]

#RAWG devuelve la imagen principal aca
    imagen = juego.get("background_image")
    return imagen