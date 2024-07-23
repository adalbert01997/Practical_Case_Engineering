import os
from dotenv import load_dotenv

load_dotenv()

# INEGI_API_URL = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicator_id}/es/00/false/BISE/2.0/{token}?type=json"
INEGI_API_URL = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicator_id}/es/{geo_area}/false/BISE/2.0/{token}?type=json"


BANXICO_API_URL = (
    "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF60653/datos"
)
MONGO_URI = os.getenv("MONGO_URI")

INEGI_TOKEN = os.getenv("INEGI_TOKEN")
BANXICO_TOKEN = os.getenv("BANXICO_TOKEN")

print("BANXICO_TOKEN:", BANXICO_TOKEN)
print("INEGI_TOKEN:", INEGI_TOKEN)
print("MONGO_URI:", MONGO_URI)

INDICATORS = {
    "454168": "consumer_confidence",
    "628194": "inpc_base",
    "444603": "unemployment_rate",
}
# https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/454168/es/00/BISE/1.0/3c56d87f-99b8-5a07-dfc2-ae6d94629df1?type=json
# https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/454168/es/00/BISE/1.0/3c56d87f-99b8-5a07-dfc2-ae6d94629df1?type=json
# https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/454168/es/00/BISE/1.0/your_inegi_token_here?type=json
