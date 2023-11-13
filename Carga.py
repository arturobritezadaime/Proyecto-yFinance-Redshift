import pandas as pd
from sqlalchemy import create_engine, inspect, exc
import configparser
import logging

# Constantes
ARCHIVO_LOG = 'log.txt'


def cargar_dataframe_staging_en_redshift(dataframe, nombre_tabla):
    logging.basicConfig(filename=ARCHIVO_LOG, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='a')
    registrador = logging.getLogger(__name__)

    try:
        configuracion_redshift = obtener_configuracion_redshift()

        with create_engine(obtener_cadena_conexion(configuracion_redshift)).connect() as conexion:
            inspector = inspect(conexion)

            # Renombrar la columna 'Open' a 'Opens'
            dataframe = dataframe.rename(columns={'Open': 'Opens'})

            # Redondear o truncar las columnas según la definición de la tabla
            dataframe = redondear_columnas(dataframe)

            if inspector.has_table(nombre_tabla):
                cargar_datos(registrador, dataframe, nombre_tabla, conexion)
            else:
                crear_y_cargar_tabla(registrador, dataframe, nombre_tabla, conexion)

    except exc.SQLAlchemyError as e:
        registrador.error(f"Error de SQLAlchemy: {str(e)}")
    except Exception as e:
        registrador.error(f"Ocurrió un error inesperado: {str(e)}")


def redondear_columnas(dataframe):
    # Redondear o truncar las columnas según la definición de la tabla
    columnas_a_redondear = ['Opens', 'High', 'Low', 'Close', 'Dividends', 'Stock Splits']
    dataframe[columnas_a_redondear] = dataframe[columnas_a_redondear].fillna(0).round(6)
    dataframe['Volume'] = dataframe['Volume'].fillna(0).astype(int)
    dataframe['Dividends'] = dataframe['Dividends'].astype(float)
    dataframe['Stock Splits'] = dataframe['Stock Splits'].astype(float)
    return dataframe


def cargar_datos(registrador, dataframe, nombre_tabla, conexion):
    dataframe = dataframe.rename(columns=lambda x: x.lower())
    filas_existente = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conexion)

    nueva_fila = dataframe[~dataframe.set_index(list(dataframe.columns.str.lower())).index.isin(
        filas_existente.set_index(list(dataframe.columns.str.lower())).index)]

    if not nueva_fila.empty:
        nueva_fila.to_sql(nombre_tabla, conexion, if_exists='append', index=False, method='multi', chunksize=500)
        registrador.info(f"Datos cargados en la tabla {nombre_tabla}.")
    else:
        registrador.info(f"No hay filas nuevas para cargar en la tabla {nombre_tabla}.")


def crear_y_cargar_tabla(registrador, dataframe, nombre_tabla, conexion):
    registrador.info(f"La tabla {nombre_tabla} no existe en Redshift. Creando la tabla y cargando datos...")
    dataframe.to_sql(nombre_tabla, conexion, if_exists='replace', index=False, method='multi', chunksize=500)
    registrador.info(f"Tabla {nombre_tabla} creada y datos cargados en Redshift.")



def cargar_dataframe_accion_en_redshift(dataframe, nombre_tabla):
    """Carga datos de un DataFrame de acciones en una tabla de Redshift."""
    # Configurar el logger con fecha y hora
    logging.basicConfig(filename=ARCHIVO_LOG, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
    logger = logging.getLogger(__name__)

    try:
        redshift_config = obtener_configuracion_redshift()
        engine = create_engine(obtener_cadena_conexion(redshift_config))
        inspector = inspect(engine)

        # Truncar los valores de las columnas que superen los 512 caracteres
        dataframe['nombre_empresa'] = dataframe['nombre_empresa'].str[:100]
        dataframe['sector'] = dataframe['sector'].str[:100]
        dataframe['industria'] = dataframe['industria'].str[:100]
        dataframe['otros_detalles'] = dataframe['otros_detalles'].str[:512]

        if inspector.has_table(nombre_tabla):
            existing_ids = pd.read_sql(f"SELECT id_accion FROM {nombre_tabla}", engine)
            nueva_fila = dataframe[~dataframe['id_accion'].isin(existing_ids['id_accion'])]

            if not nueva_fila.empty:
                nueva_fila.to_sql(nombre_tabla, engine, if_exists='append', index=False)
                logger.info(f"Datos de acciones cargados en la tabla {nombre_tabla} ")
            else:
                logger.info(f"No hay acciones nuevas para cargar en la tabla {nombre_tabla}.")
        else:
            logger.info(f"La tabla {nombre_tabla} no existe en Redshift. Creando la tabla y cargando datos...")
            dataframe.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
            logger.info(f"Tabla {nombre_tabla} creada y datos cargados en Redshift.")

    except Exception as e:
        logger.error(f"Ocurrió un error: {str(e)}")


def cargar_dataframe_fecha_en_redshift(dataframe, nombre_tabla):
    """Carga datos de un DataFrame de fechas en una tabla de Redshift."""
    # Configurar el logger
    logging.basicConfig(filename=ARCHIVO_LOG, level=logging.INFO, format='%(levelname)s - %(message)s', filemode='a')
    logger = logging.getLogger(__name__)

    try:
        redshift_config = obtener_configuracion_redshift()
        engine = create_engine(obtener_cadena_conexion(redshift_config))

        query = f"SELECT fecha FROM {nombre_tabla}"
        existing_dates = pd.read_sql_query(query, con=engine)

        # Eliminar duplicados en el DataFrame antes de la carga
        dataframe = dataframe.drop_duplicates(subset=['fecha'])

        # Filtrar solo las fechas que no existen en la tabla actualmente
        nuevas_fechas = dataframe[~dataframe['fecha'].isin(existing_dates['fecha'])]

        if not nuevas_fechas.empty:
            nuevas_fechas.to_sql(nombre_tabla, engine, if_exists='append', index=False)
            logger.info(f"Datos de fechas cargados en la tabla {nombre_tabla}.")
        else:
            logger.info(f"No hay nuevas fechas para cargar en la tabla {nombre_tabla}.")

    except Exception as e:
        logger.error(f"Ocurrió un error: {str(e)}")


def cargar_dataframe_precio_acciones_en_redshift(dataframe, nombre_tabla):
    """Carga datos de un DataFrame de precios de acciones en una tabla de Redshift."""
    # Configurar el logger con fecha y hora
    logging.basicConfig(filename=ARCHIVO_LOG, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
    logger = logging.getLogger(__name__)

    try:
        redshift_config = obtener_configuracion_redshift()
        engine = create_engine(obtener_cadena_conexion(redshift_config))
        inspector = inspect(engine)

        if inspector.has_table(nombre_tabla):
            existing_rows = pd.read_sql(f"SELECT fecha, id_accion FROM {nombre_tabla}", engine)

            # Filtrar solo las filas que no existen en la tabla actualmente
            nueva_fila = dataframe[~dataframe.set_index(['fecha', 'id_accion']).index.isin(
                existing_rows.set_index(['fecha', 'id_accion']).index)]

            if not nueva_fila.empty:
                # Verificar si hay datos nuevos por fecha y acción
                coincidentes = nueva_fila.set_index(['fecha', 'id_accion']).index.isin(existing_rows.set_index(['fecha', 'id_accion']).index)

                if coincidentes.any():
                    logger.warning("Algunos datos de precios de acciones ya existen. No se cargarán.")
                else:
                    nueva_fila.to_sql(nombre_tabla, engine, if_exists='append', index=False)
                    logger.info(f"Datos de precios de acciones cargados en la tabla {nombre_tabla}.")
            else:
                logger.info(f"No hay datos nuevos para cargar en la tabla {nombre_tabla}.")
        else:
            dataframe.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
            logger.info(f"Tabla {nombre_tabla} creada y datos de precios de acciones cargados en Redshift.")

    except Exception as e:
        logger.error(f"Ocurrió un error: {str(e)}")


def obtener_configuracion_redshift():
    config = configparser.ConfigParser()
    config.read('config.ini')

    redshift_config = {
        'user': config['redshift']['user'],
        'password': config['redshift']['password'],
        'host': config['redshift']['host'],
        'port': int(config['redshift']['port']),
        'database': config['redshift']['database']
    }
    return redshift_config

def obtener_cadena_conexion(redshift_config):
    connection_string = f"postgresql://{redshift_config['user']}:{redshift_config['password']}@{redshift_config['host']}:{redshift_config['port']}/{redshift_config['database']}"
    return connection_string