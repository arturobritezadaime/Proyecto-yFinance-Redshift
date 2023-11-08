import psycopg2
import configparser

# Leer la configuración de conexión a Redshift desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Obtener la configuración de Redshift
redshift_config = {
    'user': config['redshift']['user'],
    'password': config['redshift']['password'],
    'host': config['redshift']['host'],
    'port': int(config['redshift']['port']),
    'database': config['redshift']['database']
}


# Paso 2: Crear las tablas en Redshift
def crear_tablas_redshift():
    try:
        # Establecer una conexión a Redshift
        conn = psycopg2.connect(**redshift_config)
        cursor = conn.cursor()

        # Leer el contenido del archivo Codigo_SQL.sql
        with open('Codigo_SQL.sql', 'r') as sql_file:
            sql_statements = sql_file.read()

        # Dividir el contenido del archivo en sentencias SQL individuales (separadas por punto y coma)
        sql_parts = sql_statements.split(';')

        transaction_sql = ""  # Inicializa la variable transaction_sql

        for sql_part in sql_parts:
            if sql_part.strip():  # Asegurarse de que la sentencia no esté en blanco
                transaction_sql += sql_part + ";"  # Agregar fragmentos de SQL a la transacción

                # Verificar si la sentencia contiene un COMMIT
                if "COMMIT" in sql_part:
                    cursor.execute(transaction_sql)  # Ejecutar la transacción
                    transaction_sql = ""  # Reiniciar la variable transaction_sql

        # Confirmar la transacción
        conn.commit()
        print("Tablas en Redshift creadas con éxito.")

    except (Exception, psycopg2.Error) as error:
        print("Error al crear tablas en Redshift:", error)

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    crear_tablas_redshift()
