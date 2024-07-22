import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["economic_data"]

# Formato de la URL de la API de INEGI
INEGI_API_URL = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicator_id}/es/00/true/BISE/2.0/{token}?type=json"


def get_inegi_data(indicator_id):
    url = INEGI_API_URL.format(
        indicator_id=indicator_id, token=os.getenv("INEGI_TOKEN")
    )
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            print(
                f"Conexión a la API de INEGI exitosa para el indicador {indicator_id}."
            )
            return data
        except requests.exceptions.JSONDecodeError:
            print("Error: No se pudo decodificar la respuesta JSON.")
            print("Respuesta recibida:", response.text)
    else:
        print(
            f"Error al conectar con la API de INEGI para el indicador {indicator_id}: {response.status_code}"
        )
        print("Contenido de la respuesta:", response.text)
    return None


# Función para almacenar datos en MongoDB
def store_data(collection_name, data):
    if data:
        collection = db[collection_name]
        collection.insert_many(data["Series"][0]["OBSERVATIONS"])
        print(f"Datos del indicador {collection_name} almacenados en MongoDB.")


# Indicadores (actualiza los IDs confirmados)
indicators = {
    "1002000001": "consumer_confidence",  # Ejemplo
    "1002000002": "inpc_base",  # Ejemplo
    "1002000003": "unemployment_rate",  # Ejemplo
}

# Extraer y almacenar datos
for indicator_id, collection_name in indicators.items():
    data = get_inegi_data(indicator_id)
    store_data(collection_name, data)

print("Datos extraídos y almacenados exitosamente.")
