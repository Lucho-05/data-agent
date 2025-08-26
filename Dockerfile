# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la API al contenedor
COPY . .

# Comando para ejecutar la aplicación cuando el contenedor se inicie
CMD ["python", "main.py"]