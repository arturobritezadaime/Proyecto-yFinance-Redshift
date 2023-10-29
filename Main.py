
import yfinance as yf
import pandas as pd
import configparser
from Conexion_Creacion_Tablas import crear_tablas_redshift  # Importa la función necesaria

def obtener_configuracion():
    """
    Lee la configuración desde el archivo config.ini.

    Returns:
        config (configparser.ConfigParser): Objeto de configuración.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def obtener_datos_historicos(config):
    """
    Obtiene datos históricos de precios de las empresas listadas en la configuración.

    Args:
        config (configparser.ConfigParser): Objeto de configuración.

    Returns:
        df_stock_data_staging (pandas.DataFrame): DataFrame con datos de precios de acciones.
        df_dim_fecha (pandas.DataFrame): DataFrame con información de fechas.
        df_dim_accion (pandas.DataFrame): DataFrame con información de empresas.
        df_fac_precio_acciones (pandas.DataFrame): DataFrame con precios de acciones.
    """
    fecha_inicio = config['fechas']['fecha_inicio']
    empresas_lista = eval(config['empresas']['lista'])  # Usamos eval para convertir la cadena en una lista

    df_stock_data_staging = pd.DataFrame(columns=['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits'])
    df_dim_fecha = pd.DataFrame(columns=['Fecha', 'Día', 'Mes', 'Año'])
    df_dim_accion = pd.DataFrame(columns=['Símbolo_Acción', 'Nombre_Empresa', 'Sector', 'Industria', 'Otros_Detalles'])
    df_fac_precio_acciones = pd.DataFrame(columns=['ID_Fecha', 'ID_Accion', 'Precio_Apertura', 'Precio_Máximo', 'Precio_Mínimo', 'Precio_Cierre', 'Volumen', 'Dividendos', 'Divisiones_de_Acciones'])

    fecha_final = pd.to_datetime('today').strftime('%Y-%m-%d')

    for simbolo, nombre_empresa in empresas_lista:
        # Obtener datos históricos de precios
        empresa = yf.Ticker(simbolo)
        data = empresa.history(start=fecha_inicio, end=fecha_final)

        if data is not None:
            # Llenar el DataFrame de stock_data_staging
            data['Symbol'] = simbolo
            df_stock_data_staging = pd.concat([df_stock_data_staging, data], axis=0)

            # Llenar el DataFrame de Dim_Fecha
            data['Fecha'] = data.index
            data['Día'] = data.index.day
            data['Mes'] = data.index.month
            data['Año'] = data.index.year
            df_dim_fecha = pd.concat([df_dim_fecha, data[['Fecha', 'Día', 'Mes', 'Año']]])

            # Obtener información adicional de la empresa
            info = empresa.info

            # Llenar el DataFrame de Dim_Accion
            df_dim_accion = pd.concat([df_dim_accion, pd.DataFrame({'Símbolo_Acción': [simbolo], 'Nombre_Empresa': [nombre_empresa],
                                                                  'Sector': [info.get('sector', 'N/A')],
                                                                  'Industria': [info.get('industry', 'N/A')],
                                                                  'Otros_Detalles': [info.get('longBusinessSummary', 'N/A')]})])

            # Llenar el DataFrame de Fac_Precio_Acciones
            data['ID_Accion'] = simbolo #a modo de ejemplo (debe crearse en redshift)
            df_fac_precio_acciones = pd.concat([df_fac_precio_acciones, data])

    return df_stock_data_staging, df_dim_fecha, df_dim_accion, df_fac_precio_acciones

def main():
    config = obtener_configuracion()
    df_stock_data_staging, df_dim_fecha, df_dim_accion, df_fac_precio_acciones = obtener_datos_historicos(config)

    print("DataFrame stock_data_staging:")
    print(df_stock_data_staging)

    print("\nDataFrame Dim_Fecha:")
    print(df_dim_fecha)

    print("\nDataFrame Dim_Accion:")
    print(df_dim_accion)

    print("\nDataFrame Fac_Precio_Acciones:")
    print(df_fac_precio_acciones)
    # Llama a la función de Conexion_Creacion_Tablas para crear las tablas en Redshift
    crear_tablas_redshift()
if __name__ == "__main__":
    main()

