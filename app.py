from flask import Flask, request, jsonify
from flask_cors import CORS
from contact import create_contact_by_phone, create_contact_by_email

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de CORS para permitir únicamente alphaqueb.com
CORS(app, resources={
    r"/*": {
        "origins": "https://alphaqueb.com"  # Solo permitir este dominio
    }
})

# Ruta para crear contacto por teléfono
@app.route('/create_contact_phone', methods=['POST'])
def create_contact_phone():
    try:
        data = request.json
        country_code = data.get('country_code')
        phone_number = data.get('phone_number')

        if not country_code or not phone_number:
            return jsonify({'status': 'error', 'message': 'El código de país y el número de teléfono son obligatorios'}), 400

        contact_id = create_contact_by_phone(country_code, phone_number)

        return jsonify({'status': 'success', 'contact_id': contact_id}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Ruta para crear contacto por email
@app.route('/create_contact_email', methods=['POST'])
def create_contact_email():
    try:
        data = request.json
        email = data.get('email')
        message = data.get('message')

        if not email or not message:
            return jsonify({'status': 'error', 'message': 'El correo electrónico y el mensaje son obligatorios'}), 400

        contact_id = create_contact_by_email(email, message)

        return jsonify({'status': 'success', 'contact_id': contact_id}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
