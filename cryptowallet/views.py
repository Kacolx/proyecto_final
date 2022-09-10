from . import app


@app.route("/")
def inicio():
    return "pagina de inicio"


@app.route("/purchase", methods=["GET", "POST"])
def compra():
    return "formulario de compra"


@app.route("/status")
def estado():
    return "estado de la invercion"
