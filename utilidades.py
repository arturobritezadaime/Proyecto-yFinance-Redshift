
import configparser
import logging

ARCHIVO_LOG = 'log.txt'
def obtener_configuracion_redshift():
    """
    Obtiene la configuración de Redshift desde un archivo de configuración.
    """
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
    """
    Construye la cadena de conexión para Redshift.
    """
    connection_string = f"postgresql://{redshift_config['user']}:{redshift_config['password']}@" \
                        f"{redshift_config['host']}:{redshift_config['port']}/{redshift_config['database']}"
    return connection_string

def configurar_logger():
    """Configura el logger con fecha y hora."""
    logging.basicConfig(filename=ARCHIVO_LOG, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

