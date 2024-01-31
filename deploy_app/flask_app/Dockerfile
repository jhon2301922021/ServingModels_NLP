FROM python:3.10-slim

# Copy local code to the container image.
WORKDIR /app
COPY . .

# Install production dependencies.
RUN pip install --upgrade pip

# Install production dependencies.
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside the container
EXPOSE 8000

# Run Gunicorn to serve the Flask app
CMD exec gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --timeout 0 app:app