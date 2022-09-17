import sqlite3
import requests
from . import APIKEY


class CriptoModel:
    """
    - moneda origen
    - moneda destino
    - cambio
    - consultar cambio (método)
    """

    def __init__(self):
        """
        Construye un objeto con las monedas origen y destino
        y el cambio obtenido desde CoinAPI inicializado a cero.
        """
        self.moneda_from = ""
        self.moneda_to = ""
        self.cambio = 0.0

    def consultar_cambio(self, moneda_from, moneda_to):
        """
        Consulta el cambio entre la moneda origen y la moneda destino
        utilizando la API REST CoinAPI.
        """

        self.moneda_from = moneda_from
        self.moneda_to = moneda_to
        cabeceras = {
            "X-CoinAPI-Key": APIKEY
        }
        url = f"http://rest.coinapi.io/v1/exchangerate/{self.moneda_from}/{self.moneda_to}"
        respuesta = requests.get(url, headers=cabeceras)

        if respuesta.status_code == 200:
            # guardo el cambio obtenido
            self.cambio = respuesta.json()["rate"]
        else:
            raise ValueError(
                "Ha ocurrido un error {} {} al consultar la API.".format(
                    respuesta.status_code, respuesta.reason
                )
            )


class DBManager:
    def __init__(self, ruta):
        self.ruta = ruta

    def consultaSQL(self, consulta):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)

        self.cryptocambios = []
        nombres_columnas = []

        for desc_columna in cursor.description:
            nombres_columnas.append(desc_columna[0])

        datos = cursor.fetchall()
        for dato in datos:
            cryptocambio = {}
            indice = 0
            for nombre in nombres_columnas:
                cryptocambio[nombre] = dato[indice]
                indice += 1
            self.cryptocambios.append(cryptocambio)

        conexion.close()

        return self.cryptocambios

    def consultaConParametros(self, consulta, params):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as error:
            print("ERROR DB:", error)
            conexion.rollback()
        conexion.close()

        return resultado

    def obtenerMovimientoPorMoneda(self, moneda):

        consulta = "SELECT SUM(cantidad_from) FROM crypto WHERE moneda_from=?"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (moneda,))

        datos = cursor.fetchone()
        resultado = False

        if datos:
            nombres_columnas = []

            for desc_columna in cursor.description:
                nombres_columnas.append(desc_columna[0])

            movimiento = {}
            indice = 0
            for nombre in nombres_columnas:
                movimiento[nombre.strip('SUM()')] = datos[indice]
                indice += 1
            resultado = movimiento

        conexion.close()
        return resultado

    def consultaConParametrosStatus(self, consulta, params):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = 0
        try:
            cursor.execute(consulta, params)
            dato = cursor.fetchone()
            resultado = dato[0]
        except Exception as error:
            print("ERROR DB:", error)
            conexion.rollback()
        conexion.close()

        return resultado
