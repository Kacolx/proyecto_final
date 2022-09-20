from flask import Flask


RUTA = 'data/crypto.db'

MONEDAS_TO = [("BTC",), ("ETH",), ("BNB",)]


app = Flask(__name__)
app.config.from_prefixed_env()
