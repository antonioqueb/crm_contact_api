import os
import xmlrpc.client
from dotenv import load_dotenv
import logging

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Variables de entorno de Odoo
odoo_url = os.getenv('ODOO_URL')
db = os.getenv('ODOO_DB')
username = os.getenv('ODOO_USERNAME')
password = os.getenv('ODOO_PASSWORD')

logging.debug(f"Intentando conectar a Odoo en {odoo_url} con la base de datos '{db}' y el usuario '{username}'")

try:
    # Conectar con el servidor de Odoo
    common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    if uid:
        logging.info(f"Autenticado en Odoo con UID: {uid}")
    else:
        logging.error("Falló la autenticación en Odoo. Verifica las credenciales.")
        raise Exception("Falló la autenticación en Odoo")

    # Conectar con los modelos de Odoo
    models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')

except Exception as e:
    logging.exception("Error al conectar con Odoo")
    raise e  # Re-lanzamos la excepción para que sea manejada en el nivel superior
