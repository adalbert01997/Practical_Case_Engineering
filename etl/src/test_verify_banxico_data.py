import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["economic_data"]


def verify_banxico_data():
    collection = db["banxico"]
    data = collection.find()
    for record in data:
        print(record)


print("Datos en la colección banxico:")
verify_banxico_data()
print("Verificación de datos en MongoDB completada.")
