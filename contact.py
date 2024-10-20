from config import models, db, uid, password

# Crear contacto por número de teléfono
def create_contact_by_phone(country_code, phone_number, user_id=None, company_id=None):
    # Formatear el número de teléfono completo
    full_phone = f"+{country_code} {phone_number}"

    # Definir los datos del contacto a crear
    contact_data = {
        'name': f"Contacto {full_phone}",
        'phone': full_phone,
        'customer': True  # Se crea como cliente
    }

    # Si se proporcionan user_id y company_id, los agregamos
    if user_id:
        contact_data['user_id'] = user_id
    if company_id:
        contact_data['company_id'] = company_id

    # Crear el contacto en Odoo
    contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [contact_data])
    
    return contact_id

# Crear contacto por correo electrónico y mensaje
def create_contact_by_email(email, message, user_id=None, company_id=None):
    # Definir los datos del contacto a crear
    contact_data = {
        'name': f"Contacto {email}",
        'email': email,
        'comment': message,  # Guardar el mensaje en el campo 'comentario'
        'customer': True  # Se crea como cliente
    }

    # Si se proporcionan user_id y company_id, los agregamos
    if user_id:
        contact_data['user_id'] = user_id
    if company_id:
        contact_data['company_id'] = company_id

    # Crear el contacto en Odoo
    contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [contact_data])

    return contact_id
