from flask import Flask
APIKEY = '831CA601-C095-40A9-9A9C-94FED492B61E'

# '714D8ADA-CC9C-40FE-BCCA-846022573268'

MONEDAS_TO = [("BTC",), ("ETH",), ("BNB",)]


app = Flask(__name__)
app.config.from_prefixed_env()
