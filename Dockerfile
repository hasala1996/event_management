FROM python:slim-buster

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar y instalar las dependencias
COPY requeriments/requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt

# Copiar el código de la aplicación al contenedor
COPY . .

# Establecer el directorio de trabajo en /app/src
WORKDIR /app/src

# Comando por defecto para ejecutar migraciones y arrancar el servidor
CMD ["sh", "-c", "python manage.py wait_for_db && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]