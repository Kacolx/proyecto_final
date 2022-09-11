from flask import render_template
from . import app
from .models import DBManager

RUTA = 'data/crypto.db'


@app.route("/")
def inicio():
    db = DBManager(RUTA)
    cambios = db.consultaSQL("SELECT * FROM crypto")
    return render_template("inicio.html", movs=cambios)


@app.route("/purchase", methods=["GET", "POST"])
def compra():
    return "formulario de compra"


@app.route("/status")
def estado():
    return "estado de la invercion"
