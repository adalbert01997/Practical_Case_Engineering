import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["economic_data"]


def verify_mongo_data(collection_name):
    collection = db[collection_name]
    data = collection.find()
    for record in data:
        print(record)


# Colecciones a verificar
collections = ["consumer_confidence", "inpc_base", "unemployment_rate"]
for collection in collections:
    print(f"Datos en la colección {collection}:")
    verify_mongo_data(collection)
    print("\n")

print("Verificación de datos en MongoDB completada.")
