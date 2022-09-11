import sqlite3


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
