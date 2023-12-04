# Utiliza una imagen oficial de Apache Airflow
FROM apache/airflow:latest

# Actualiza pip
RUN pip install --upgrade pip

# Copia todo el contenido del proyecto al contenedor
COPY . /opt/airflow/

# Establece el directorio de trabajo
WORKDIR /opt/airflow/

# Instala las dependencias desde requirements-full.txt que en realidad cargo las librerias necesarias
RUN pip install --no-cache-dir -r requirements-full.txt

# Configura el usuario de Airflow
USER airflow
