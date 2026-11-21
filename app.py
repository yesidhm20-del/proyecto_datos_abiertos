from flask import Flask, render_template, request, redirect, url_for, flash
from api.api_client import APIClient
from models.datos_model import guardar_registros, consultar_registros, obtener_resumen

app = Flask(__name__)
app.secret_key = "clave-local-proyecto-datos-abiertos"


@app.route("/", methods=["GET"])
def inicio():
    filtro = request.args.get("q", "").strip()
    try:
        registros = consultar_registros(filtro)
        resumen = obtener_resumen()
    except Exception as error:
        registros = []
        resumen = {"total": 0, "departamentos": 0, "top": []}
        flash(f"No fue posible consultar la base de datos: {error}", "error")
    return render_template(
        "index.html", registros=registros, filtro=filtro, resumen=resumen
    )


@app.route("/sincronizar", methods=["POST"])
def sincronizar():
    try:
        cliente = APIClient()
        datos = cliente.obtener_registros()
        cantidad = guardar_registros(datos)
        flash(f"Consulta terminada. Nuevos registros guardados: {cantidad}", "success")
    except Exception as error:
        flash(f"No fue posible consultar o guardar los datos: {error}", "error")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
