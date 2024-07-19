import requests
from pymongo import MongoClient
from constants import BANXICO_API_URL, INEGI_API_URL, MONGO_URI, INDICATORS


def get_banxico_data():
    response = requests.get(BANXICO_API_URL)
    data = response.json()
    return data["bmx"]["series"][0]["datos"]


def get_inegi_data(indicator_id):
    url = INEGI_API_URL.format(
        indicator_id=indicator_id,
        geographic_code="00",
        version_api="1.0",
        token=os.getenv("INEGI_TOKEN"),
    )
    response = requests.get(url)
    data = response.json()
    return data["Series"][0]["OBSERVATIONS"]


client = MongoClient(MONGO_URI)
db = client["economic_data"]

# Extracción y almacenamiento de datos
banxico_data = get_banxico_data()
db.banxico.insert_many(banxico_data)

for indicator_id, collection_name in INDICATORS.items():
    inegi_data = get_inegi_data(indicator_id)
    db[collection_name].insert_many(inegi_data)

print("Datos extraídos y almacenados exitosamente.")
