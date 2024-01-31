# Importar las bibliotecas necesarias para la aplicación web y la autenticación de Google
from flask import Flask, redirect, session, request
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Obtener variable de entorno
REDIRECT_URL = os.getenv('REDIRECT_URL')

# Inicializar la aplicación Flask
app = Flask(__name__)
# Establecer una clave secreta para la sesión; se utiliza para mantener la información de la sesión segura
app.secret_key = 'some_random_secret'

# Función para inicializar el cliente OAuth2
def get_flow():
    # Definir el alcance (scope) para el acceso a Gmail, solo lectura en este caso
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    # Crear el flujo de autenticación utilizando las credenciales del archivo y el alcance definido
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', 
                                                     scopes = SCOPES,
                                                     redirect_uri = f'{REDIRECT_URL}/callback')
    return flow

# Definir una ruta en la raíz que maneje las solicitudes GET
@app.route('/', methods=["GET"])
def start_auth():
    # Iniciar el flujo de autenticación de OAuth2
    flow = get_flow()
    # Obtener la URL de autorización y el estado
    authorization_url, state = flow.authorization_url(
        access_type='offline', # Permitir el acceso sin conexión para obtener un token de refresco
        prompt='consent' # Forzar al usuario a dar su consentimiento
    )
    # Guardar el estado en la sesión para su uso posterior
    session['state'] = state
    # Redirigir al usuario a la URL de autorización
    return redirect(authorization_url)

# Definir una ruta para el callback de OAuth2
@app.route('/callback', methods=["GET", "POST"])
def callback():
    # Recuperar el flujo de autenticación
    flow = get_flow()
    # Obtener el estado guardado en la sesión
    state = session['state']
    # Canjear el código por un token y actualizar el flujo con el token obtenido
    flow.fetch_token(code=request.args.get('code'), state=state)
    # Guardar las credenciales en la sesión y convertirlas a JSON
    session['credentials'] = flow.credentials.to_json()
    # Devolver las credenciales como respuesta
    return session['credentials']