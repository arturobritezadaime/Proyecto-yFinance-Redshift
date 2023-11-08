import requests
import yfinance as yf
import pandas as pd
import configparser
from datetime import datetime
import Conexion_Creacion_Tablas  # Importar el módulo de creación de tablas
from Carga import cargar_dataframe_accion_en_redshift, cargar_dataframe_fecha_en_redshift, \
    cargar_dataframe_precio_acciones_en_redshift

def obtener_configuracion():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def obtener_info_acciones(config):
    api_key = config['alpha_vantage']['api_key']
    empresas_lista = eval(config['empresas']['lista'])

    df_dim_acciones = pd.DataFrame(
        columns=['id_accion','simbolo_accion', 'nombre_empresa', 'sector', 'industria', 'otros_detalles'])
    id_accion = 1
    for simbolo, _ in empresas_lista:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={simbolo}&apikey={api_key}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            new_row = {
                'id_accion': id_accion,
                'simbolo_accion': data.get("Symbol", "N/A"),
                'nombre_empresa': data.get("Name", "N/A"),
                'sector': data.get("Sector", "N/A"),
                'industria': data.get("Industry", "N/A"),
                'otros_detalles': data.get("Description", "N/A")
            }

            df_dim_acciones = pd.concat([df_dim_acciones, pd.DataFrame([new_row])], ignore_index=True)
            id_accion += 1
        else:
            print(f"Error al obtener datos para el símbolo {simbolo}. Código de estado:", response.status_code)

    return df_dim_acciones


def obtener_datos_historicos(config):
    fecha_inicio = config['fechas']['fecha_inicio']
    empresas_lista = eval(config['empresas']['lista'])

    df_stock_data_staging = pd.DataFrame(
        columns=['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
    df_dim_fecha = pd.DataFrame(columns=['fecha', 'dia', 'mes', 'anio'])
    df_fac_precio_acciones = pd.DataFrame(
        columns=['fecha', 'id_accion', 'precio_apertura', 'precio_maximo', 'precio_minimo', 'precio_cierre', 'volumen',
                 'dividendos', 'divisiones_de_acciones'])

    fecha_final = pd.to_datetime('today').strftime('%Y-%m-%d')
    id_accion = 1
    for simbolo, _ in empresas_lista:
        empresa = yf.Ticker(simbolo)
        data = empresa.history(start=fecha_inicio, end=fecha_final)

        if data is not None:
            data['Symbol'] = simbolo
            df_stock_data_staging = pd.concat([df_stock_data_staging, data], axis=0)

            data['fecha'] = data.index
            data['dia'] = data.index.day
            data['mes'] = data.index.month
            data['anio'] = data.index.year
            df_dim_fecha = pd.concat([df_dim_fecha, data[['fecha', 'dia', 'mes', 'anio']]])
            data.rename(columns={'Open': 'precio_apertura', 'High': 'precio_maximo', 'Low': 'precio_minimo',
                                 'Close': 'precio_cierre', 'Volume': 'volumen', 'Dividends': 'dividendos',
                                 'Stock Splits': 'divisiones_de_acciones'}, inplace=True)
            data['id_accion'] = id_accion
            # Redondear las columnas numéricas al segundo decimal
            columns_to_round = ['precio_apertura', 'precio_maximo', 'precio_minimo', 'precio_cierre', 'volumen',
                                'dividendos', 'divisiones_de_acciones']
            df_fac_precio_acciones[columns_to_round] = df_fac_precio_acciones[columns_to_round].round(2)
            df_fac_precio_acciones = pd.concat([df_fac_precio_acciones, data.drop(['dia', 'mes', 'anio'], axis=1)])
            df_fac_precio_acciones.drop(columns=['Symbol'], inplace=True)


            id_accion += 1
    return df_stock_data_staging, df_dim_fecha, df_fac_precio_acciones

def guardar_dataframes_en_excel(df_stock_data_staging, df_dim_fecha, df_fac_precio_acciones, df_dim_acciones, nombre_archivo):
    """
    Guarda los DataFrames en un archivo Excel con hojas separadas.

    Args:
        df_stock_data_staging (pandas.DataFrame): DataFrame de datos de precios de acciones.
        df_dim_fecha (pandas.DataFrame): DataFrame de información de fechas.
        df_fac_precio_acciones (pandas.DataFrame): DataFrame de precios de acciones.
        df_dim_acciones (pandas.DataFrame): DataFrame de información de empresas.
        nombre_archivo (str): Nombre del archivo Excel de salida.
    """
    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:

        df_stock_data_staging['Date'] = df_stock_data_staging.index  # Crear la columna 'Date' a partir del índice
        df_stock_data_staging['Date'] = df_stock_data_staging['Date'].dt.date #Eliminar la zona horaria y la hora de las fechas
        df_dim_fecha['fecha'] = df_dim_fecha['fecha'].dt.date #Eliminar la zona horaria y la hora de las fechas
        df_fac_precio_acciones['fecha'] = df_fac_precio_acciones['fecha'].dt.date #Eliminar la zona horaria y la hora de las fechas

        df_dim_fecha.to_excel(writer, sheet_name='Dim_Fecha', index=False)
        df_stock_data_staging.to_excel(writer, sheet_name='Stock_Data_Staging', index=False)
        df_fac_precio_acciones.to_excel(writer, sheet_name='Fac_Precio_Acciones', index=False)
        df_dim_acciones.to_excel(writer, sheet_name='Dim_Acciones', index=False)

def main():
    config = obtener_configuracion()

    # Obtener información de las acciones desde Alpha Vantage
    df_dim_acciones = obtener_info_acciones(config)

    if not df_dim_acciones.empty:
        print("DataFrame Dim_Acciones:")
        print(df_dim_acciones)

    # Obtener la fecha y hora actual en el formato 'YY-MM-DD HH-MM-SS'
    fecha_hora_actual = datetime.now().strftime('%y-%m-%d %H-%M-%S')
    nombre_archivo = f'datos_empresa_{fecha_hora_actual}.xlsx'
    # Obtener datos históricos de Yahoo Finance
    df_stock_data_staging, df_dim_fecha, df_fac_precio_acciones = obtener_datos_historicos(config)
    guardar_dataframes_en_excel(df_stock_data_staging, df_dim_fecha, df_fac_precio_acciones, df_dim_acciones,
                                nombre_archivo)
    print("DataFrame stock_data_staging:")
    print(df_stock_data_staging)

    print("\nDataFrame Dim_Fecha:")
    print(df_dim_fecha)

    print("\nDataFrame Fac_Precio_Acciones:")
    print(df_fac_precio_acciones)
    # Crear las tablas en Redshift
    Conexion_Creacion_Tablas.crear_tablas_redshift()
# Realizar la carga de datos en Redshift
    cargar_dataframe_accion_en_redshift(df_dim_acciones, 'dim_accion')
    cargar_dataframe_fecha_en_redshift(df_dim_fecha, 'dim_fecha')
    cargar_dataframe_precio_acciones_en_redshift(df_fac_precio_acciones, 'fac_precio_acciones')

if __name__ == "__main__":
    main()
