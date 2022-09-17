

from datetime import date, datetime, time


from flask import render_template, request, flash, redirect, url_for

from .form import CambiosForm
from . import app, MONEDAS_TO
from .models import DBManager, CriptoModel

RUTA = 'data/crypto.db'


@app.route("/")
def inicio():
    try:
        db = DBManager(RUTA)
        cambios = db.consultaSQL("SELECT * FROM crypto")

        return render_template("inicio.html", movs=cambios)
    except:
        flash("No se pueden cargar los movimientos", category="Error consulta")
        return render_template("inicio.html")


@app.route("/purchase", methods=["GET", "POST"])
def compra():
    if request.method == "GET":
        formulario = CambiosForm()

        return render_template("purchase.html", form=formulario)

    else:
        formulario = CambiosForm(data=request.form)
        if formulario.validate():

            moneda_from = formulario.moneda_from.data
            moneda_to = formulario.moneda_to.data
            cantidad_from = formulario.cantidad_from.data

            crip = CriptoModel()
            crip.consultar_cambio(moneda_from, moneda_to)
            calculo = crip.cambio
            cantidad_to = crip.cambio * cantidad_from

            if formulario.consultar_api.data:

                return render_template("purchase.html", form=formulario, PU=calculo, cantidad_to=cantidad_to)

            if formulario.comprar.data:

                db = DBManager(RUTA)

                fecha = date.today().isoformat()
                hora = time(
                    datetime.now().hour,
                    datetime.now().minute
                )
                consulta = 'INSERT INTO crypto(fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?, ?, ?, ?, ?, ?)'
                params = (fecha, str(hora), moneda_from,
                          cantidad_from, moneda_to, cantidad_to)
                guardar_compra = db.consultaConParametros(consulta, params)
                if guardar_compra:
                    return redirect("/")
            else:
                flash(message="fallo consulta a la api")
                return redirect("/purchase")

        else:
            flash("Antes de comprar debes consultar el cambio")
            return render_template("purchase.html", form=formulario, errores=["Ha fallado la consulta a la api"])


@app.route("/status")
def estado():
    db = DBManager(RUTA)
    crip = CriptoModel
    consulta = db.obtenerMovimientoPorMoneda("EUR")

    # for moneda in MONEDAS_TO:
    #     dic_moneda = db.obtenerMovimientoPorMoneda(moneda)

    return render_template("status.html", mov=consulta)
