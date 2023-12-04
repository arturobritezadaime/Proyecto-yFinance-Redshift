
def redondear_columnas(dataframe):
    columnas_a_redondear = ['Opens', 'High', 'Low', 'Close', 'Dividends', 'Stock Splits']
    dataframe[columnas_a_redondear] = dataframe[columnas_a_redondear].fillna(0).round(6)
    dataframe['Volume'] = dataframe['Volume'].fillna(0).astype(int)
    dataframe['Dividends'] = dataframe['Dividends'].astype(float)
    dataframe['Stock Splits'] = dataframe['Stock Splits'].astype(float)
    return dataframe

def truncar_columnas(dataframe, columnas, longitudes):
    for col, longitud in zip(columnas, longitudes):
        dataframe[col] = dataframe[col].str[:longitud]
