# Genera las evidencias automáticamente. Ejecutar: python generar_evidencias.py
import os
import json
from api.api_client import APIClient
from models.datos_model import guardar_registros, consultar_registros, obtener_resumen

os.makedirs("evidencias", exist_ok=True)

cliente = APIClient()
datos = cliente.obtener_registros()
with open("evidencias/evidencia_json_api.json", "w", encoding="utf-8") as f:
    json.dump(datos[:5], f, indent=2, ensure_ascii=False)
print("1) JSON de la API recibido:", len(datos), "registros (muestra guardada en evidencias/evidencia_json_api.json)")

primera = guardar_registros(datos)
segunda = guardar_registros(datos)
print("2) Primera sincronización, registros nuevos:", primera)
print("3) Segunda sincronización, registros nuevos (debe ser 0):", segunda)

resumen = obtener_resumen()
registros = consultar_registros()
with open("evidencias/evidencia_registros_sql.txt", "w", encoding="utf-8") as f:
    f.write("Primera sincronización, nuevos: %s\n" % primera)
    f.write("Segunda sincronización, nuevos: %s (sin duplicados)\n\n" % segunda)
    f.write("Total en RegistrosAPI: %s | Departamentos: %s\n\n" % (resumen["total"], resumen["departamentos"]))
    for r in registros[:20]:
        f.write("%s | %s | %s | %s\n" % (r["id_api"], r["municipio"], r["departamento"], r["tipo_municipio"]))
print("4) Registros guardados en SQL Server en evidencias/evidencia_registros_sql.txt")
