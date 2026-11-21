import os
import requests
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    """Se comunica con la API de datos.gov.co (Socrata/SODA)."""

    def __init__(self):
        recurso = os.getenv("API_RESOURCE_ID")
        self.url = f"https://www.datos.gov.co/resource/{recurso}.json"
        self.limite = int(os.getenv("API_LIMITE", "100"))

    def obtener_registros(self, limite=None):
        parametros = {"$limit": limite or self.limite}
        respuesta = requests.get(self.url, params=parametros, timeout=20)
        respuesta.raise_for_status()  # lanza error si el servidor responde 404, 429, etc.
        return respuesta.json()       # lista de diccionarios de Python
