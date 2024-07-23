import pymongo

# URI de conexión
mongo_uri = "mongodb+srv://adalgonlu:r21YJVTawiXagQTU@practicalcaseengineering.yhhdx46.mongodb.net/economic_data?retryWrites=true&w=majority&appName=PracticalCaseEngineering"

# Intentar conectar a la base de datos
try:
    client = pymongo.MongoClient(mongo_uri)
    db = client["economic_data"]
    collections = db.list_collection_names()
    print("Conexión exitosa. Colecciones disponibles:", collections)
except Exception as e:
    print("Error al conectar con MongoDB Atlas:", e)
