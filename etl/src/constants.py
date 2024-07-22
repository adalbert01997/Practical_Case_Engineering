import os

BANXICO_API_URL = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF60653/datos?token={os.getenv('BANXICO_TOKEN')}"
INEGI_API_URL = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicator_id}/es/{geographic_code}/BISE/{version_api}/{token}?type=json"
MONGO_URI = os.getenv("MONGO_URI")
INDICATORS = {
    "454168": "consumer_confidence",
    "628194": "inpc_base",
    "444603": "unemployment_rate",
}
