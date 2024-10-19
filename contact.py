from config import models, db, uid, password

# Crear contacto por número de teléfono
def create_contact_by_phone(country_code, phone_number):
    # Formatear el número de teléfono completo
    full_phone = f"+{country_code} {phone_number}"

    # Crear el contacto en Odoo
    contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
        'name': f"Contacto {full_phone}",
        'phone': full_phone,
        'customer': True  # Se crea como cliente
    }])
    
    return contact_id

# Crear contacto por correo electrónico y mensaje
def create_contact_by_email(email, message):
    # Crear el contacto en Odoo
    contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
        'name': f"Contacto {email}",
        'email': email,
        'comment': message,  # Guardar el mensaje en el campo 'comentario'
        'customer': True  # Se crea como cliente
    }])

    return contact_id
