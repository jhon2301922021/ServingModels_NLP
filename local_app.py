# Importar módulos necesarios
import streamlit as st  # Biblioteca para crear aplicaciones web
from utils import gmail_authenticate, get_last_n_emails, get_value_for_key  # Funciones auxiliares
from googleapiclient.discovery import build  # Para crear clientes de servicio para las APIs de Google
from transformers import pipeline  # Para usar modelos de procesamiento de lenguaje natural

# Configuración inicial de la página de Streamlit
st.set_page_config(layout='wide')

# Inicializar variables en el estado de la sesión si aún no existen
if "GMAIL_msg" not in st.session_state:
    st.session_state.GMAIL_msg = list()
if "Load_msg" not in st.session_state:
    st.session_state.Load_msg = False

# Mostrar el título de la aplicación en la página web
st.title('NLP Streamlit App')

# Crear un campo de entrada en la interfaz para que el usuario ingrese el número de correos a analizar
n_mails = st.text_input('Ingrese el número de correos a analizar')

# Crear un contenedor en Streamlit para organizar los elementos de la interfaz
with st.container():
    # Crear dos columnas en la interfaz
    col1, col2 = st.columns(2)
    with col1:
        # Crear un botón y definir la acción al hacer clic
        if st.button('Obtener correos'):
            # Construir un cliente de servicio para interactuar con la API de Gmail
            service = build('gmail', 'v1', credentials=gmail_authenticate())
            # Llamar a la función para obtener los últimos 'n_mails' correos electrónicos
            msg = get_last_n_emails(service=service, n_mails=n_mails)
            # Almacenar los correos electrónicos en el estado de la sesión
            st.session_state.GMAIL_msg = msg
            st.session_state.Load_msg = True

        # Verificar si se han cargado los mensajes y mostrarlos
        if st.session_state.get('Load_msg', False):
            # Iterar sobre cada correo y mostrar detalles
            for message in st.session_state.GMAIL_msg:
                message_dict = dict(message)
                email_headers = message_dict['payload']['headers']
                # Obtener el asunto del correo
                subject = get_value_for_key(email_headers, 'Subject')
                # Obtener el contenido resumido del correo
                content = message_dict['snippet']
                # Mostrar el asunto y el contenido en la interfaz
                st.write(f"""
                         ###################################\n
                        **Tema de correo** : {subject}\n
                        **Contenido Corto** : {content}\n\n
                        """)

    with col2:
        # Crear un botón para clasificar correos y definir la acción al hacer clic
        if st.button('Clasificar correos'):
            # Cargar un modelo de clasificación de texto
            pipe = pipeline("text-classification", model="roberta-base-openai-detector")
            # Iterar sobre cada correo para clasificar su contenido
            for message in st.session_state.GMAIL_msg:
                message_dict = dict(message)
                email_headers = message_dict['payload']['headers']
                subject = get_value_for_key(email_headers, 'Subject')
                content = message_dict['snippet']

                # Clasificar el contenido del correo
                class_ = pipe(content)
                # Mostrar el asunto del correo y su clasificación en la interfaz
                st.write(f"""
                         ###################################\n
                        **Tema de correo** : {subject}\n
                        **Clasificación** : {str(class_[0])}\n\n
                        """)
