import configparser
import os


ARCHIVO = 'configuracion.ini' # no modificar

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__),ARCHIVO))

HILOS = int(config['red']['HILOS'])
TIMEOUT = float(config['red']['TIMEOUT'])
FILTRADOS = config['archivos']['FILTRADOS']
COLOR = config['personalizacion']['COLOR']
ESCAN_TIMEOUT = int(config['red']['TIEMPO_DE_ESCANER'])

