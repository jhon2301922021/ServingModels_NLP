# Usar una imagen oficial de Python como imagen base
# FROM tensorflow:2.15.0
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copiar el contenido del directorio actual en el contenedor en /usr/src/app
COPY . .

# Instalar cualquier otro paquete necesario especificado en requirements.txt
# Se usa --no-cache-dir para no almacenar los archivos de caché de pip, reduciendo el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Predescarga el modelo a la imagen.
RUN python -c "from transformers import pipeline; pipeline('text-classification', model='roberta-base-openai-detector')"

# Hacer disponible el puerto 8501 al mundo exterior a este contenedor
EXPOSE 8501

# Ejecutar app.py cuando se inicie el contenedor
CMD ["streamlit", "run", "web_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]