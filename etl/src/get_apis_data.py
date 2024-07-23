import requests
from constants import (
    INEGI_API_URL,
    BANXICO_API_URL,
    INEGI_TOKEN,
    BANXICO_TOKEN,
    MONGO_URI,
)
from clean_and_store_data import clean_data, store_data
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def get_inegi_data(indicator_id, geo_area="0700"):
    url = INEGI_API_URL.format(
        indicator_id=indicator_id, geo_area=geo_area, token=INEGI_TOKEN
    )
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            series = data.get("Series", [])
            if not series:
                raise ValueError("No 'Series' data found in response.")
            observations = series[0].get("OBSERVATIONS", [])
            if not observations:
                raise ValueError("No 'OBSERVATIONS' data found in 'Series'.")
            return observations
        except (ValueError, KeyError, requests.exceptions.JSONDecodeError) as e:
            print(f"Error parsing INEGI response for indicator {indicator_id}: {e}")
            print(f"Response content: {response.text}")
            return []
    else:
        print(
            f"Error connecting to INEGI API for indicator {indicator_id}: {response.status_code}"
        )
        print(f"Response content: {response.text}")
        return []


def get_banxico_data():
    headers = {"Bmx-Token": BANXICO_TOKEN}
    response = requests.get(BANXICO_API_URL, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            series = data.get("bmx", {}).get("series", [])
            if not series:
                raise ValueError("No 'series' data found in response.")
            datos = series[0].get("datos", [])
            if not datos:
                raise ValueError("No 'datos' data found in 'series'.")
            return datos
        except (ValueError, KeyError, requests.exceptions.JSONDecodeError) as e:
            print(f"Error parsing Banxico response: {e}")
            print(f"Response content: {response.text}")
            return []
    else:
        print(f"Error connecting to Banxico API: {response.status_code}")
        print(f"Response content: {response.text}")
        return []


if __name__ == "__main__":
    # Verificar conexión a MongoDB
    try:
        client = MongoClient(MONGO_URI)
        client.server_info()  # Intenta obtener información del servidor para verificar la conexión
        print("Conexión a MongoDB Atlas exitosa.")
    except Exception as e:
        print(f"Error al conectar con MongoDB Atlas: {e}")
        exit(1)

    inegi_indicators = {
        "consumer_confidence": "1002000001",
        "PIB": "472079",
        "Gasto nacional en educación total como porcentaje del PIB": "6207067825",
    }

    for name, indicator_id in inegi_indicators.items():
        inegi_data = get_inegi_data(indicator_id, geo_area="0700")
        if inegi_data:
            cleaned_inegi_data = clean_data(inegi_data, "inegi")
            store_data(cleaned_inegi_data, name)

    banxico_data = get_banxico_data()
    if banxico_data:
        cleaned_banxico_data = clean_data(banxico_data, "banxico")
        store_data(cleaned_banxico_data, "banxico")
