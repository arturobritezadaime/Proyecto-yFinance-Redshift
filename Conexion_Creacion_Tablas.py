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

        # Crear la tabla Dim_Fecha
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Dim_Fecha (
                ID_Fecha INTEGER PRIMARY KEY,
                Fecha TIMESTAMP ENCODE az64,
                Día INTEGER ENCODE az64,
                Mes INTEGER ENCODE az64,
                Año INTEGER ENCODE az64
            )

        """)

        # Crear la tabla Dim_Accion
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Dim_Accion (
                ID_Accion INTEGER PRIMARY KEY,
                Símbolo_Acción VARCHAR(10),
                Nombre_Empresa VARCHAR(100) ENCODE lzo,
                Sector VARCHAR(100) ENCODE lzo,
                Industria VARCHAR(100) ENCODE lzo,
                Otros_Detalles TEXT ENCODE lzo
            )
            SORTKEY (Símbolo_Acción)

        """)

        # Crear la tabla Fac_Precio_Acciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Fac_Precio_Acciones (
                ID_Fecha INTEGER DISTKEY,
                ID_Accion INTEGER,
                Precio_Apertura DECIMAL(10, 2) ENCODE az64,
                Precio_Máximo DECIMAL(10, 2) ENCODE az64,
                Precio_Mínimo DECIMAL(10, 2) ENCODE az64,
                Precio_Cierre DECIMAL(10, 2) SORTKEY,
                Volumen BIGINT ENCODE az64,
                Dividendos DECIMAL(10, 2) ENCODE az64,
                Divisiones_de_Acciones DECIMAL(10, 2) ENCODE az64
            );
        """)

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