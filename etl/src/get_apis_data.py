import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["economic_data"]

# URLs y tokens de las APIs
INEGI_API_URL = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicator_id}/es/00/true/BISE/2.0/{token}?type=json"
BANXICO_API_URL_TEMPLATE = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/{series_id}/datos/{start_date}/{end_date}"
BANXICO_API_TOKEN = os.getenv("BANXICO_API_TOKEN")


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
            return data["Series"][0]["OBSERVATIONS"]
        except requests.exceptions.JSONDecodeError:
            print("Error: No se pudo decodificar la respuesta JSON.")
            print("Respuesta recibida:", response.text)
    else:
        print(
            f"Error al conectar con la API de INEGI para el indicador {indicator_id}: {response.status_code}"
        )
        print("Contenido de la respuesta:", response.text)
    return None


def get_banxico_data(series_id, start_date, end_date):
    url = BANXICO_API_URL_TEMPLATE.format(
        series_id=series_id, start_date=start_date, end_date=end_date
    )
    headers = {"Bmx-Token": BANXICO_API_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("Conexión a la API de Banxico exitosa.")
        return data["bmx"]["series"][0]["datos"]
    else:
        print(f"Error al conectar con la API de Banxico: {response.status_code}")
        print("Contenido de la respuesta:", response.text)
    return None


def store_data(collection_name, data):
    if data:
        collection = db[collection_name]
        collection.insert_many(data)
        print(f"Datos de {collection_name} almacenados en MongoDB.")


# Indicadores de INEGI (IDs de prueba)
inegi_indicators = {
    "1002000001": "consumer_confidence",
    "1002000002": "inpc_base",
    "1002000003": "unemployment_rate",
}

# Extraer y almacenar datos de INEGI
for indicator_id, collection_name in inegi_indicators.items():
    data = get_inegi_data(indicator_id)
    store_data(collection_name, data)

# Extraer y almacenar datos de Banxico (usar series_id, start_date, end_date de ejemplo)
banxico_series_id = "SF43718"  # ID de serie de ejemplo
banxico_start_date = "2020-01-01"  # Fecha de inicio de ejemplo
banxico_end_date = "2023-01-01"  # Fecha de fin de ejemplo

banxico_data = get_banxico_data(banxico_series_id, banxico_start_date, banxico_end_date)
store_data("banxico", banxico_data)

print("Proceso de extracción y almacenamiento de datos completado.")
