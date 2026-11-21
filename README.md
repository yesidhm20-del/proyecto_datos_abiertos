# Sistema Web de Consulta y Análisis de Datos Abiertos de Colombia

**Integrantes:** Crismar Vergara y Yesid Hernandez

Proyecto integrador de **Desarrollo de Aplicaciones con Acceso a Datos** (Corporación Universitaria Americana).
Tecnologías: Python, Flask, API REST (SODA), SQL Server (pyodbc) y HTML/CSS, con patrón MVC.

## 1. Objetivo
Consultar una API pública de datos.gov.co, guardar los registros recibidos en SQL Server (sin duplicarlos) y
consultarlos desde el navegador con un filtro sencillo y un resumen numérico.

## 2. Dataset elegido
- **Nombre:** DIVIPOLA – Códigos municipios (DANE)
- **Propósito:** tener el listado oficial de municipios para consultarlo y resumirlo por departamento.
- **Endpoint:** `https://www.datos.gov.co/resource/gdxc-w37w.json?$limit=100`
- **Portal:** https://www.datos.gov.co/

### Campos usados
| Campo del JSON | Columna en SQL Server | Qué representa |
|---|---|---|
| `cod_mpio` | `id_api` (UNIQUE) | Código DIVIPOLA del municipio; evita duplicados |
| `nom_mpio` | `municipio` | Nombre del municipio |
| `dpto` | `departamento` | Nombre del departamento |
| `tipo_municipio` | `tipo_municipio` | Tipo (municipio, área no municipalizada, etc.) |
| `latitud` | `latitud` | Latitud del centroide |
| `longitud` | `longitud` | Longitud del centroide |
| (todo el registro) | `json_original` | Copia completa del JSON recibido |

> Antes de entregar, ejecuten `python probar_api.py` y confirmen que los nombres de campos coinciden con el JSON real.
> Si alguno difiere, ajusten el mapeo en `models/datos_model.py` (función `guardar_registros`).

## 3. Requisitos
Python 3.10+, Visual Studio Code, SQL Server + SQL Server Management Studio (SSMS),
Microsoft ODBC Driver 18 for SQL Server y un navegador.

## 4. Instalación
1. Abrir una terminal en la carpeta del proyecto.
2. Crear y activar el entorno virtual:
   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Instalar dependencias: `pip install -r requirements.txt`
4. En SSMS: botón **Nueva consulta**, abrir/pegar `sql/crear_base_datos.sql` y pulsar **Ejecutar**.
5. Copiar `.env.example` como `.env` y ajustar `DB_SERVER`, `DB_TRUSTED`, `DB_USER` y `DB_PASSWORD`
   (autenticación de Windows: `DB_TRUSTED=yes`; autenticación SQL: `DB_TRUSTED=no` y usuario/contraseña).
   **No subir `.env` a repositorios.**

## 5. Ejecución
1. `python app.py`
2. Abrir http://127.0.0.1:5000
3. Pulsar **Consultar API y guardar datos** y revisar el mensaje.
4. Verificar en SSMS: `SELECT * FROM RegistrosAPI;`
5. Probar el buscador y volver a sincronizar para comprobar que no se duplican registros.

Para cargar todos los municipios (~1122) cambien `API_LIMITE` en `.env` (por ejemplo, 1200).

## 6. Estructura MVC
```
proyecto_datos_abiertos/
├── app.py                 # CONTROLADOR: rutas Flask (/ y /sincronizar)
├── api/api_client.py      # Servicio: consume la API externa
├── models/datos_model.py  # MODELO: conexión y consultas a SQL Server
├── templates/index.html   # VISTA: HTML (Jinja2)
├── static/estilos.css     # Estilos
├── sql/                   # crear_base_datos.sql y consultar_registros.sql
├── probar_api.py          # Prueba rápida y evidencia del JSON
├── generar_evidencias.py  # Genera las evidencias (JSON y registros)
├── evidencias/            # JSON, registros y capturas
├── .env.example
├── requirements.txt
└── README.md
```
- **Modelo:** abre la conexión, guarda registros (evitando duplicados) y ejecuta los SELECT. No genera HTML.
- **Vista:** solo muestra datos con `{{ }}` y `{% %}`; no tiene SQL ni se conecta a la base de datos.
- **Controlador:** recibe la petición del navegador, llama a `APIClient` o al Modelo y elige la plantilla.

## 7. Distribución del trabajo
- **Crismar Vergara:** API y datos (selección del dataset, `api_client.py`, lectura del JSON) y la Vista (`index.html`).
- **Yesid Hernandez:** SQL Server y Modelo (script SQL, conexión pyodbc, inserción sin duplicados, consultas) y el Controlador (`app.py`).
- **Trabajo conjunto:** integración, pruebas, documentación y sustentación.

## 8. Entregables
- [x] Código fuente con la estructura solicitada
- [x] Script SQL (`sql/crear_base_datos.sql`)
- [x] `requirements.txt` (sin contraseñas)
- [x] README
- [x] Evidencia del JSON de la API: `evidencias/evidencia_json_api.json`
- [x] Evidencia de registros en SQL Server: `evidencias/06_registros_sql_server_1122_filas.png` y `evidencias/evidencia_registros_sql.txt`
- [x] Capturas de la web: sincronización (`04_...`), página principal con resumen (`02_...` y `04_...`) y consulta filtrada (`05_...`)
- [x] Detalle de cada archivo en `evidencias/LEEME_evidencias.md`

## 9. Errores frecuentes
| Problema | Qué revisar |
|---|---|
| ModuleNotFoundError | Activar el entorno virtual e instalar dependencias |
| Data source name not found | Instalar ODBC Driver y que `DB_DRIVER` coincida exactamente |
| Login failed | Autenticación de Windows o usuario/contraseña |
| Invalid object name | Que la tabla esté creada en `DatosAbiertosDB` |
| HTTP 404 / 429 | Revisar `API_RESOURCE_ID` / reducir frecuencia y límite |
