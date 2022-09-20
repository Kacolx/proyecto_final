# Proyecto_final
## CRYPTO WALLET

Proyecto con flask classic, simulacion de billetera virtual

## Para arrancar la aplicación

1. Generar y activar un entorno virtual
1. Instalar el archivo requirements.txt desde la consola de comandos 
   <!-- pip install - r requirements.txt -->
2. Copiar el archivo `.env_template` a `.env` y establecer los valores adecuados (`FLASK_APP=main`)
4. visita la pagina CoinAPI y consigue gratis tu APIKEY
5. Creaccion de base de datos
- Descargar e intalar  SQlite desde https://www.sqlite.org/index.html 
- Descarga DB browser for SQlite desde https://sqlitebrowser.org/dl/
-  tienes una base de datos incluida en el repo con una par de movimientos realizados
- O puedes abrir el DB browser for SQlite y crear la base de datos dentro del directorio del proyecto dentro  una carpeta `data` con la siguiente sentencia de creacion (si usas esta opcion recuerda borrar la base de datos incluida en el repo)
CREATE TABLE "crypto" (
	"id"	INTEGER NOT NULL,
	"fecha"	TEXT NOT NULL,
	"hora"	TEXT NOT NULL,
	"moneda_from"	TEXT NOT NULL,
	"cantidad_from"	NUMERIC NOT NULL,
	"moneda_to"	TEXT NOT NULL,
	"cantidad_to"	NUMERIC NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)
6. Copiar el archivo `config_template.py` a `config.py` y poner tu API KEY

7. Ejecutar la aplicación con `flask run`

```shell
python -m venv env

# linux / macos
source ./env/bin/activate
cp .env_template .env

# Windows
.\env\Scripts\activate
copy .env_template .env

flask run
```