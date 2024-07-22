import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Añadir el directorio 'etl/src' al sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Verificar las variables de entorno cargadas
print("BANXICO_TOKEN:", os.getenv("BANXICO_TOKEN"))
print("INEGI_TOKEN:", os.getenv("INEGI_TOKEN"))
print("MONGO_URI:", os.getenv("MONGO_URI"))

from constants import BANXICO_API_URL
import requests


def test_banxico_connection():
    print("BANXICO_API_URL:", BANXICO_API_URL)
    response = requests.get(BANXICO_API_URL)
    if response.status_code == 200:
        data = response.json()
        print("Conexión a la API de Banxico exitosa.")
        print(data)
    else:
        print("Error al conectar con la API de Banxico:", response.status_code)


if __name__ == "__main__":
    test_banxico_connection()
