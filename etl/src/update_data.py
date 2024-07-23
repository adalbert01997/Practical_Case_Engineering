import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging
from clean_and_store_data import clean_data, store_data
from constants import (
    INEGI_API_URL,
    BANXICO_API_URL_TEMPLATE,
    INEGI_TOKEN,
    BANXICO_API_TOKEN,
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

# Load environment variables from .env file
load_dotenv()
logging.info("Environment variables loaded.")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["economic_data"]
logging.info("Connected to MongoDB.")


# Function to get INEGI data
def get_inegi_data(indicator_id):
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


# Function to get Banxico data
def get_banxico_data(series_id, start_date, end_date):
    url = BANXICO_API_URL_TEMPLATE.format(
        series_id=series_id, start_date=start_date, end_date=end_date
    )
    headers = {"Bmx-Token": BANXICO_API_TOKEN}
    response = requests.get(url, headers=headers)
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


def main():
    logging.info("Starting data extraction process.")
    try:
        # Update INEGI data
        inegi_indicators = {
            "consumer_confidence": "1002000001",
            "PIB": "472079",
            "Gasto nacional en educación total como porcentaje del PIB": "6207067825",
        }
        # Extract and store INEGI data
        for indicator_id, collection_name in inegi_indicators.items():
            data = get_inegi_data(indicator_id)
            if data:
                db[collection_name].delete_many({})  # Remove old data
                cleaned_data = clean_data(data, "inegi")
                store_data(cleaned_data, collection_name)

        # Update Banxico data
        banxico_series_id = "SF43718"  # Example series ID
        banxico_start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        banxico_end_date = datetime.now().strftime("%Y-%m-%d")

        banxico_data = get_banxico_data(
            banxico_series_id, banxico_start_date, banxico_end_date
        )
        if banxico_data:
            db["banxico"].delete_many({})  # Remove old data
            cleaned_data = clean_data(banxico_data, "banxico")
            store_data(cleaned_data, "banxico")

        logging.info("Data update completed.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        client.close()  # Close MongoDB connection
        logging.info("MongoDB connection closed.")


if __name__ == "__main__":
    main()
