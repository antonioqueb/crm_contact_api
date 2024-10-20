from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from contact import create_contact_by_phone, create_contact_by_email

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

# Ruta para crear contacto por teléfono
@app.route('/create_contact_phone', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://alphaqueb.com', methods=['POST', 'OPTIONS'], headers=['Content-Type', 'Authorization'])
def create_contact_phone():
    if request.method == 'OPTIONS':
        # Responder a la solicitud preflight
        return jsonify({'status': 'ok'}), 200

    try:
        data = request.json
        country_code = data.get('country_code')
        phone_number = data.get('phone_number')
        user_id = data.get('user_id')  # Opcional
        company_id = data.get('company_id')  # Opcional

        if not country_code or not phone_number:
            return jsonify({'status': 'error', 'message': 'El código de país y el número de teléfono son obligatorios'}), 400

        contact_id = create_contact_by_phone(country_code, phone_number, user_id, company_id)

        return jsonify({'status': 'success', 'contact_id': contact_id}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta para crear contacto por email
@app.route('/create_contact_email', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://alphaqueb.com', methods=['POST', 'OPTIONS'], headers=['Content-Type', 'Authorization'])
def create_contact_email():
    if request.method == 'OPTIONS':
        # Responder a la solicitud preflight
        return jsonify({'status': 'ok'}), 200

    try:
        data = request.json
        email = data.get('email')
        message = data.get('message')
        user_id = data.get('user_id')  # Opcional
        company_id = data.get('company_id')  # Opcional

        if not email or not message:
            return jsonify({'status': 'error', 'message': 'El correo electrónico y el mensaje son obligatorios'}), 400

        contact_id = create_contact_by_email(email, message, user_id, company_id)

        return jsonify({'status': 'success', 'contact_id': contact_id}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Manejador global de errores para incluir encabezados CORS en respuestas de error
@app.errorhandler(Exception)
@cross_origin(origin='https://alphaqueb.com')
def handle_exception(e):
    response = jsonify({'status': 'error', 'message': str(e)})
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
