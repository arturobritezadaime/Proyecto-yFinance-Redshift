import configparser
import logging
import os

ARCHIVO_LOG = 'log.txt'


def obtener_configuracion_redshift():
    """
    Obtiene la configuración de Redshift desde un archivo de configuración.
    """
    # Obtener la ruta del directorio del script
    directorio_script = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta completa al archivo config.ini
    ruta_config = os.path.join(directorio_script, '..', 'config', 'config.ini')

    # Verificar si el archivo config.ini existe
    if not os.path.isfile(ruta_config):
        print(f"Error: No se encontró el archivo de configuración: {ruta_config}")
        exit()
    config = configparser.ConfigParser()
    config.read(ruta_config)

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
    """
    Configura el logger para el registro de eventos.

    Returns:
        logging.Logger: Objeto logger configurado.
    """
    logging.basicConfig(filename=ARCHIVO_LOG, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='a')
    return logging.getLogger(__name__)
