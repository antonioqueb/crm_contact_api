import logging
from config import models, db, uid, password

# Crear contacto por número de teléfono
def create_contact_by_phone(country_code, phone_number, user_id=None, company_id=None):
    try:
        # Formatear el número de teléfono completo
        full_phone = f"+{country_code} {phone_number}"
        logging.debug(f"Creando contacto con teléfono: {full_phone}")

        # Definir los datos del contacto a crear
        contact_data = {
            'name': f"Contacto {full_phone}",
            'phone': full_phone,
            'customer_rank': 1  # Se crea como cliente
        }

        # Si se proporcionan user_id y company_id, los agregamos
        if user_id:
            contact_data['user_id'] = user_id
        if company_id:
            contact_data['company_id'] = company_id

        logging.debug(f"Datos del contacto a crear: {contact_data}")

        # Crear el contacto en Odoo
        contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [contact_data])
        logging.info(f"Contacto creado en Odoo con ID: {contact_id}")

        return contact_id

    except Exception as e:
        logging.exception("Error en create_contact_by_phone")
        raise e  # Re-lanzamos la excepción para que sea manejada en el nivel superior

# Crear oportunidad en CRM con nombre, email y mensaje
def create_lead(name, email, message, user_id=None, company_id=None):
    try:
        logging.debug(f"Creando oportunidad con nombre: {name}, email: {email}")

        # Definir los datos de la oportunidad a crear
        lead_data = {
            'name': f"Oportunidad de {name}",
            'contact_name': name,
            'email_from': email,
            'description': message,  # Guardar el mensaje en el campo 'description'
            'type': 'lead',  # Tipo de oportunidad
        }

        # Si se proporcionan user_id y company_id, los agregamos
        if user_id:
            lead_data['user_id'] = user_id
        if company_id:
            lead_data['company_id'] = company_id

        logging.debug(f"Datos de la oportunidad a crear: {lead_data}")

        # Crear la oportunidad en Odoo
        lead_id = models.execute_kw(db, uid, password, 'crm.lead', 'create', [lead_data])
        logging.info(f"Oportunidad creada en Odoo con ID: {lead_id}")

        return lead_id

    except Exception as e:
        logging.exception("Error en create_lead")
        raise e  # Re-lanzamos la excepción para que sea manejada en el nivel superior
