import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging
from clean_and_store_data import clean_data, store_data
from constants import (
    INEGI_API_URL,
    BANXICO_API_URL,
    INEGI_TOKEN,
    BANXICO_TOKEN,
    MONGO_URI,
)

# Configurar logging
log_file_path = os.path.join(os.path.dirname(__file__), "update_data.log")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

logging.info("Starting update_data script.")

# Cargar variables de entorno desde el archivo .env
load_dotenv()
logging.info("Environment variables loaded.")

# Conectar a MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client["economic_data"]
    logging.info("Connected to MongoDB.")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    exit(1)


def get_inegi_data(indicator_id):
    logging.info(f"Fetching INEGI data for indicator {indicator_id}")
    url = INEGI_API_URL.format(indicator_id=indicator_id, token=INEGI_TOKEN)
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
            logging.info(
                f"Successful connection to INEGI API for indicator {indicator_id}."
            )
            return observations
        except (ValueError, KeyError, requests.exceptions.JSONDecodeError) as e:
            logging.error(
                f"Error parsing INEGI response for indicator {indicator_id}: {e}"
            )
            logging.error("Response content: %s", response.text)
    else:
        logging.error(
            f"Error connecting to INEGI API for indicator {indicator_id}: {response.status_code}"
        )
        logging.error("Response content: %s", response.text)
    return None


def get_banxico_data():
    logging.info("Fetching Banxico data")
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
            logging.info("Successful connection to Banxico API.")
            return datos
        except (ValueError, KeyError, requests.exceptions.JSONDecodeError) as e:
            logging.error(f"Error parsing Banxico response: {e}")
            logging.error("Response content: %s", response.text)
    else:
        logging.error(f"Error connecting to Banxico API: {response.status_code}")
        logging.error("Response content: %s", response.text)
    return None


def store_data(df, collection_name):
    logging.info(f"Storing data in collection {collection_name}")
    collection = db[collection_name]
    try:
        collection.insert_many(df.to_dict("records"), ordered=False)
        logging.info(f"New data for {collection_name} stored in MongoDB.")
    except Exception as e:
        logging.error(f"Error storing data in collection {collection_name}: {e}")


def main():
    logging.info("Starting data extraction process.")
    try:
        # Actualizar datos de INEGI
        inegi_indicators = {
            "consumer_confidence": "1002000001",
            "PIB": "472079",
            "Gasto nacional en educación total como porcentaje del PIB": "6207067825",
        }
        for collection_name, indicator_id in inegi_indicators.items():
            logging.info(f"Processing INEGI indicator {indicator_id}")
            data = get_inegi_data(indicator_id)
            if data:
                logging.info(f"Cleaning data for INEGI indicator {indicator_id}")
                cleaned_data = clean_data(data, "inegi")
                logging.info(
                    f"Storing data for INEGI indicator {indicator_id} in collection {collection_name}"
                )
                store_data(cleaned_data, collection_name)

        # Actualizar datos de Banxico
        logging.info("Processing Banxico data")
        banxico_data = get_banxico_data()
        if banxico_data:
            logging.info("Cleaning data for Banxico")
            cleaned_data = clean_data(banxico_data, "banxico")
            logging.info("Storing data for Banxico in collection banxico")
            store_data(cleaned_data, "banxico")

        logging.info("Data update completed.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        client.close()  # Cerrar conexión a MongoDB
        logging.info("MongoDB connection closed.")
        print("Script completed successfully.")


if __name__ == "__main__":
    main()
