# Utiliza una imagen base oficial de Python 3.9
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requirements.txt al directorio de trabajo
COPY requirements.txt ./

# Instalar las dependencias requeridas
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación Flask
COPY . .

# Exponer el puerto 5000 para que Flask esté disponible externamente
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
