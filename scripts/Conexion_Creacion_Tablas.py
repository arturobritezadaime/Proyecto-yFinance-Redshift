import psycopg2
import utilidades

def dividir_sql(sql_statements):
    """
    Divide el contenido del archivo en sentencias SQL individuales.
    """
    return [sql.strip() for sql in sql_statements.split(';') if sql.strip()]

def ejecutar_transaccion(cursor, transaction_sql):
    """
    Ejecuta una transacción SQL en el cursor.
    """
    cursor.execute(transaction_sql)

def crear_tablas_redshift():
    """
    Crea las tablas en Redshift.
    """
    try:
        # Configurar el logger desde utilidades.py
        logger = utilidades.configurar_logger()

        # Obtener la configuración de Redshift desde utilidades.py
        redshift_config = utilidades.obtener_configuracion_redshift()

        # Establecer una conexión a Redshift
        with psycopg2.connect(**redshift_config) as conn:
            with conn.cursor() as cursor:
                # Leer el contenido del archivo Codigo_SQL.sql
                with open('Codigo_SQL.sql', 'r') as sql_file:
                    sql_statements = sql_file.read()

                # Dividir el contenido del archivo en sentencias SQL individuales
                sql_parts = dividir_sql(sql_statements)

                transaction_sql = ""  # Inicializa la variable transaction_sql

                for sql_part in sql_parts:
                    transaction_sql += sql_part + ";"

                    # Verificar si la sentencia contiene un COMMIT
                    if "COMMIT" in sql_part:
                        ejecutar_transaccion(cursor, transaction_sql)
                        transaction_sql = ""  # Reiniciar la variable transaction_sql

                # Confirmar la transacción
                conn.commit()
                logger.info("Tablas en Redshift creadas con éxito.")

    except (Exception, psycopg2.Error) as error:
        logger.error("Error al crear tablas en Redshift: %s", error)

if __name__ == "__main__":
    crear_tablas_redshift()
