# Importar la clase InstalledAppFlow de la biblioteca google_auth_oauthlib
from google_auth_oauthlib.flow import InstalledAppFlow
# Importar el módulo base64 para codificar y decodificar datos
import base64

# Función para recuperar los últimos 'n_mails' correos electrónicos
def get_last_n_emails(service, n_mails):
    # Solicitar la lista de mensajes para el usuario autenticado, limitado por 'n_mails'
    results = service.users().messages().list(userId='me', maxResults=n_mails).execute()
    # Obtener los mensajes de la respuesta de la API
    messages = results.get('messages', [])
    total_msg = []  # Lista para almacenar los mensajes procesados

    # Iterar sobre cada mensaje en la lista de mensajes
    for message in messages:
        # Obtener los detalles completos del mensaje usando su ID
        msg = service.users().messages().get(userId='me', id=message['id']).execute()

        # Extraer el payload y las partes del mensaje
        payload = msg.get('payload', {})
        parts = payload.get('parts', [])
        body = ""  # Variable para almacenar el cuerpo del mensaje
        # Verificar si hay datos codificados en base64 en el cuerpo del mensaje
        if 'data' in payload['body']:
            # Decodificar los datos del cuerpo del mensaje
            body = base64.urlsafe_b64decode(payload['body']['data']).decode("utf-8")
        else:
            # Iterar sobre las partes del mensaje para encontrar y decodificar el texto
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode("utf-8")
                    break
        
        # Agregar el cuerpo del mensaje decodificado al diccionario del mensaje
        msg["body"] = body

        # Añadir el mensaje procesado a la lista total_msg
        total_msg.append(msg)
    # Devolver la lista de mensajes procesados
    return total_msg

# Función para obtener un valor específico de los encabezados de un correo electrónico
def get_value_for_key(email_headers, key):
    # Iterar sobre cada encabezado en los encabezados del correo electrónico
    for header in email_headers:
        # Verificar si el nombre del encabezado coincide con la clave buscada
        if header['name'] == key:
            # Devolver el valor del encabezado si se encuentra la clave
            return header['value']
    # Devolver None si no se encuentra la clave
    return None