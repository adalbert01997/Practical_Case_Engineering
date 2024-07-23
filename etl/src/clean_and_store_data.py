import pandas as pd
from pymongo import MongoClient
from constants import MONGO_URI


def clean_data(data, source):
    df = pd.DataFrame(data)

    # Ejemplo de limpieza y normalización
    if source == "banxico":
        df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")
        df["dato"] = df["dato"].astype(float)
    elif source == "inegi":
        df = df.rename(
            columns={
                "TIME_PERIOD": "time_period",
                "OBS_VALUE": "obs_value",
                "OBS_EXCEPTION": "obs_exception",
                "OBS_STATUS": "obs_status",
                "OBS_SOURCE": "obs_source",
                "OBS_NOTE": "obs_note",
            }
        )
        df["time_period"] = pd.to_datetime(df["time_period"], format="%Y")
        df["obs_value"] = df["obs_value"].astype(float)

    # Imprimir datos limpios
    print(f"\nCleaned data from {source}:")
    print(df.head())
    return df


def store_data(df, collection_name):
    client = MongoClient(MONGO_URI)
    db = client["economic_data"]
    collection = db[collection_name]

    # Visualizar los datos antes de almacenarlos
    print(f"Data to be stored in collection {collection_name}:")
    print(df.head())

    collection.delete_many({})
    collection.insert_many(df.to_dict("records"))
    print(f"Datos almacenados en la colección {collection_name}.")
