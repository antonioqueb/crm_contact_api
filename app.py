from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from contact import create_contact_by_phone, create_lead  # Importar funciones desde contact.py
import logging
import os

# Configurar el logging
logging.basicConfig(level=logging.DEBUG)

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de CORS para permitir únicamente alphaqueb.com
CORS(app, resources={
    r"/*": {
        "origins": "https://alphaqueb.com",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Ruta para crear contacto por teléfono y oportunidad en CRM
@app.route('/create_contact_phone', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://alphaqueb.com', methods=['POST', 'OPTIONS'], headers=['Content-Type', 'Authorization'])
def create_contact_phone_route():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    try:
        data = request.get_json()
        logging.debug(f"Datos recibidos en /create_contact_phone: {data}")
        country_code = data.get('country_code')
        phone_number = data.get('phone_number')
        user_id = data.get('user_id')  # Opcional
        company_id = data.get('company_id')  # Opcional

        logging.debug(f"country_code: {country_code}, phone_number: {phone_number}, user_id: {user_id}, company_id: {company_id}")

        if not country_code or not phone_number:
            mensaje_error = 'El código de país y el número de teléfono son obligatorios'
            logging.error(mensaje_error)
            return jsonify({'status': 'error', 'message': mensaje_error}), 400

        contact_id, lead_id = create_contact_by_phone(country_code, phone_number, user_id, company_id)
        logging.info(f"Contacto y oportunidad creados con IDs: {contact_id}, {lead_id}")

        return jsonify({'status': 'success', 'contact_id': contact_id, 'lead_id': lead_id}), 201

    except Exception as e:
        logging.exception("Error en create_contact_phone_route")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta para crear oportunidad en CRM
@app.route('/create_lead', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://alphaqueb.com', methods=['POST', 'OPTIONS'], headers=['Content-Type', 'Authorization'])
def create_lead_route():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    try:
        data = request.get_json()
        logging.debug(f"Datos recibidos en /create_lead: {data}")
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        user_id = data.get('user_id')  # Opcional
        company_id = data.get('company_id')  # Opcional

        logging.debug(f"name: {name}, email: {email}, message: {message}, user_id: {user_id}, company_id: {company_id}")

        if not name or not email or not message:
            mensaje_error = 'El nombre, correo electrónico y mensaje son obligatorios'
            logging.error(mensaje_error)
            return jsonify({'status': 'error', 'message': mensaje_error}), 400

        lead_id = create_lead(name, email, message, user_id, company_id)
        logging.info(f"Oportunidad creada con ID: {lead_id}")

        return jsonify({'status': 'success', 'lead_id': lead_id}), 201

    except Exception as e:
        logging.exception("Error en create_lead_route")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Manejador global de errores para incluir encabezados CORS en respuestas de error
@app.errorhandler(Exception)
@cross_origin(origin='https://alphaqueb.com')
def handle_exception(e):
    logging.exception("Excepción global capturada")
    response = jsonify({'status': 'error', 'message': str(e)})
    response.status_code = 500
    return response

if __name__ == '__main__':
    # Imprimir variables de entorno para Odoo (sin mostrar la contraseña por seguridad)
    odoo_url = os.getenv('ODOO_URL')
    db = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USERNAME')
    # password = os.getenv('ODOO_PASSWORD')  # No imprimas la contraseña

    logging.debug(f"Variables de entorno - ODOO_URL: {odoo_url}, ODOO_DB: {db}, ODOO_USERNAME: {username}")

    app.run(host='0.0.0.0', port=5000, debug=True)
