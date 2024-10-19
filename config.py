import os
import xmlrpc.client
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Variables de entorno de Odoo
odoo_url = os.getenv('ODOO_URL')
db = os.getenv('ODOO_DB')
username = os.getenv('ODOO_USERNAME')
password = os.getenv('ODOO_PASSWORD')

# Conectar con el servidor de Odoo
common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

# Conectar con los modelos de Odoo
models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')
