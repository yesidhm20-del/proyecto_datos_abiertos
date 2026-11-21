# Prueba rápida de la API (opcional). Ejecutar: python probar_api.py
import json
from api.api_client import APIClient

cliente = APIClient()
datos = cliente.obtener_registros(5)

print("Cantidad recibida:", len(datos))
if datos:
    print(json.dumps(datos[0], indent=2, ensure_ascii=False))
    with open("evidencia_json_api.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
    print("Evidencia guardada en evidencia_json_api.json")
else:
    print("La API no devolvió registros")
