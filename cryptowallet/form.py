
from flask_wtf import FlaskForm
from wtforms import SubmitField,  FloatField,  SelectField, DateField, TimeField
from wtforms.validators import DataRequired


class CambiosForm(FlaskForm):

    fecha = DateField("Fecha")
    hora = TimeField("Hora")
    moneda_from = SelectField(
        "From: ", choices=[("EUR", "EUR"), ("BTC", "BTC"), ("ETH", "ETH"), ("BNB", "BNB")],
        validators=[DataRequired(message="selecciona una moneda")],)
    moneda_to = SelectField(
        "To: ",  choices=[("BTC", "BTC"), ("ETH", "ETH"), ("BNB", "BNB")],
        validators=[DataRequired(message="selecciona una moneda")],)
    cantidad_from = FloatField(
        "Q from", validators=[DataRequired(message="escribe la cantidad")], )

    cantidad_to = FloatField(
        "Q",
    )
    consultar_api = SubmitField("Consultar", render_kw={
                                "class": "blue-button"})

    PU = FloatField("PU: ")
    comprar = SubmitField("Comprar", render_kw={
        "class": "green-button"})


class StatusForm(FlaskForm):
    consultar = SubmitField("Consultar", render_kw={
        "class": "blue-button"})
