from .api_client import APIClient

def main():
    api = APIClient()
    juegos = api.obtener_juegos()

    print("Juegos recibidos desde la API:")
    for j in juegos:
        print(f"- ({j['id']}) {j['nombre']} - {j['genero']}")

if __name__ == "__main__":
    main()