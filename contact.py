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

        # Crear una oportunidad en el CRM asociada al contacto
        lead_data = {
            'name': f"Oportunidad de {full_phone}",
            'contact_name': f"Contacto {full_phone}",
            'partner_id': contact_id,  # Asociar la oportunidad al contacto creado
            'phone': full_phone,
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

        return contact_id, lead_id  # Retornamos ambos IDs

    except Exception as e:
        logging.exception("Error en create_contact_by_phone")
        raise e  # Re-lanzamos la excepción para que sea manejada en el nivel superior

# Crear oportunidad en CRM con nombre, email y mensaje
def create_lead(name, email, message, user_id=None, company_id=None):
    try:
        logging.debug(f"Creando oportunidad con nombre: {name}, email: {email}")

        # Buscar si ya existe un contacto con el email proporcionado
        existing_partner_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', email]]])
        if existing_partner_ids:
            partner_id = existing_partner_ids[0]
            logging.info(f"Contacto existente encontrado con ID: {partner_id}")
        else:
            # Si no existe, crear un nuevo contacto
            partner_data = {
                'name': name,
                'email': email,
                'customer_rank': 1
            }
            if user_id:
                partner_data['user_id'] = user_id
            if company_id:
                partner_data['company_id'] = company_id

            logging.debug(f"Datos del contacto a crear: {partner_data}")

            partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [partner_data])
            logging.info(f"Contacto creado en Odoo con ID: {partner_id}")

        # Definir los datos de la oportunidad a crear
        lead_data = {
            'name': f"Oportunidad de {name}",
            'contact_name': name,
            'partner_id': partner_id,  # Asociar la oportunidad al contacto
            'email_from': email,
            'description': message,  # Guardar el mensaje en el campo 'description'
            'type': 'lead',  # Tipo de oportunidad
        }

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
