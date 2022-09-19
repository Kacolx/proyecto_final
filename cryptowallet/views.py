

from datetime import date, datetime, time


from flask import render_template, request, flash, redirect, url_for

from .form import CambiosForm, StatusForm
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
        if not formulario.validate():
            flash("No se pudo validar el formulario")
            return redirect("/purchase")

        db = DBManager(RUTA)
        crip = CriptoModel()
        consulta_from = "SELECT SUM(cantidad_from) FROM crypto WHERE moneda_from=?"
        moneda_from = formulario.moneda_from.data

        consulta_moneda_from = db.consultaConParametrosStatus(
            consulta_from, moneda_from)

        moneda_to = formulario.moneda_to.data
        cantidad_from = formulario.cantidad_from.data

        crip.consultar_cambio(moneda_from, moneda_to)
        calculo = crip.cambio
        cantidad_to = crip.cambio * cantidad_from

        if formulario.moneda_from.data == formulario.moneda_to.data:
            flash("Las monedas no pueden se iguales")
            return redirect("/purchase")

        if formulario.consultar_api.data:
            formulario.cantidad_from.render_kw = {"readonly": True}

            return render_template("purchase.html", form=formulario, PU=calculo, cantidad_to=cantidad_to)

        if formulario.comprar.data:
            if consulta_moneda_from < cantidad_from and moneda_from != "EUR":
                flash(
                    f"No tienes suficiente {moneda_from}, para hacer esta compra")
                return redirect("/purchase")

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
                flash("no se puedo realizar la compra")
                return render_template("purchase.html", form=formulario, errores=["Ha fallado la compra"])


@app.route("/status", methods=["GET", "POST"])
def estado():
    # euro = "EUR"
    consulta_from = "SELECT SUM(cantidad_from) FROM crypto WHERE moneda_from=?"
    consulta_to = "SELECT SUM(cantidad_to) FROM crypto WHERE moneda_to=?"
    db = DBManager(RUTA)
    if request.method == 'GET':
        form = StatusForm()

        return render_template("status.html", form=form, mov=0, cantidad=0)
    else:
        form = StatusForm(data=request.form)

        if form.consultar.data:

            parametros = ("EUR",)
            consulta = db.consultaConParametrosStatus(
                consulta_from, parametros)
            euros_invertidos = consulta

            euros_en_cripto = 0

            crip = CriptoModel()
            balance_euros = 0
            for moneda in MONEDAS_TO:
                cantidad_from = db.consultaConParametrosStatus(
                    consulta_from, moneda)
                print(cantidad_from)
                cantidad_to = db.consultaConParametrosStatus(
                    consulta_to, moneda)
                print(cantidad_to)
                cantidad_moneda = cantidad_from - cantidad_to
                crip.consultar_cambio(
                    moneda_from=moneda[0], moneda_to="EUR")
                cambio = crip.cambio
                balance = cantidad_moneda * cambio
                balance_euros += balance

                # cantidad = cantidad_moneda * cambio

            return render_template("status.html", form=form, mov=euros_invertidos, cantidad=balance_euros)
