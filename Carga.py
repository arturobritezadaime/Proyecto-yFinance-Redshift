import pandas as pd
from sqlalchemy import create_engine, inspect
import configparser

def cargar_dataframe_accion_en_redshift(dataframe, nombre_tabla):
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

        nueva_fila.to_sql(nombre_tabla, engine, if_exists='append', index=False)
        print(f"Datos de acciones cargados en la tabla {nombre_tabla}.")
    else:
        print(f"La tabla {nombre_tabla} no existe en Redshift. Creando la tabla y cargando datos...")
        dataframe.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
        print(f"Tabla {nombre_tabla} creada y datos cargados en Redshift.")

def cargar_dataframe_fecha_en_redshift(dataframe, nombre_tabla):
    redshift_config = obtener_configuracion_redshift()
    engine = create_engine(obtener_cadena_conexion(redshift_config))

    query = f"SELECT fecha FROM {nombre_tabla}"
    existing_dates = pd.read_sql_query(query, con=engine)

    nueva_fila = dataframe[~dataframe['fecha'].isin(existing_dates['fecha'])]
    nueva_fila.to_sql(nombre_tabla, engine, if_exists='append', index=False)
    print(f"Datos de fechas cargados en la tabla {nombre_tabla}.")

def cargar_dataframe_precio_acciones_en_redshift(dataframe, nombre_tabla):
    redshift_config = obtener_configuracion_redshift()
    engine = create_engine(obtener_cadena_conexion(redshift_config))

    inspector = inspect(engine)

    if inspector.has_table(nombre_tabla):
        existing_rows = pd.read_sql(f"SELECT fecha, id_accion FROM {nombre_tabla}", engine)
        nueva_fila = dataframe[~dataframe.set_index(['fecha', 'id_accion']).index.isin(
            existing_rows.set_index(['fecha', 'id_accion']).index)]
        nueva_fila.to_sql(nombre_tabla, engine, if_exists='append', index=False)
        print(f"Datos de precios de acciones cargados en la tabla {nombre_tabla}.")
    else:
        dataframe.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
        print(f"Tabla {nombre_tabla} creada y datos de precios de acciones cargados en Redshift.")

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