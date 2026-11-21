import os
import json
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    servidor = os.getenv("DB_SERVER")
    base_datos = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    trusted = os.getenv("DB_TRUSTED", "yes").lower() == "yes"

    if trusted:
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    else:
        usuario = os.getenv("DB_USER")
        clave = os.getenv("DB_PASSWORD")
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            f"UID={usuario};PWD={clave};"
            "TrustServerCertificate=yes;"
        )

    return pyodbc.connect(cadena)


def guardar_registros(registros):
    """Guarda en SQL Server los registros de la API. Omite los que ya existen (id_api)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    insertados = 0

    try:
        for registro in registros:
            identificador = str(registro.get("cod_mpio") or registro.get("id") or "")
            if not identificador:
                continue

            cursor.execute(
                """
                IF NOT EXISTS (SELECT 1 FROM RegistrosAPI WHERE id_api = ?)
                INSERT INTO RegistrosAPI
                    (id_api, municipio, departamento, tipo_municipio,
                     latitud, longitud, json_original)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                identificador,
                identificador,
                registro.get("nom_mpio"),
                registro.get("dpto"),
                registro.get("tipo_municipio"),
                registro.get("latitud"),
                registro.get("longitud"),
                json.dumps(registro, ensure_ascii=False),
            )
            if cursor.rowcount > 0:
                insertados += 1

        conexion.commit()
        return insertados
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def consultar_registros(filtro=""):
    """Devuelve hasta 100 registros guardados; opcionalmente filtrados por municipio o departamento."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        if filtro:
            cursor.execute(
                """
                SELECT TOP 100 id_api, municipio, departamento,
                       tipo_municipio, latitud, longitud
                FROM RegistrosAPI
                WHERE municipio LIKE ? OR departamento LIKE ?
                ORDER BY municipio
                """,
                f"%{filtro}%",
                f"%{filtro}%",
            )
        else:
            cursor.execute(
                """
                SELECT TOP 100 id_api, municipio, departamento,
                       tipo_municipio, latitud, longitud
                FROM RegistrosAPI
                ORDER BY municipio
                """
            )

        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()


def obtener_resumen():
    """Resumen numérico: total de registros, departamentos distintos y top 5 de departamentos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT COUNT(*), COUNT(DISTINCT departamento) FROM RegistrosAPI"
        )
        total, departamentos = cursor.fetchone()

        cursor.execute(
            """
            SELECT TOP 5 departamento, COUNT(*) AS cantidad
            FROM RegistrosAPI
            WHERE departamento IS NOT NULL
            GROUP BY departamento
            ORDER BY cantidad DESC, departamento
            """
        )
        top = [{"departamento": f[0], "cantidad": f[1]} for f in cursor.fetchall()]

        return {"total": total, "departamentos": departamentos, "top": top}
    finally:
        cursor.close()
        conexion.close()
