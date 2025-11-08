import configparser


ARCHIVO = 'configuracion.ini' # no modificar

config = configparser.ConfigParser()
config.read(ARCHIVO)

HILOS = int(config['red']['HILOS'])
TIMEOUT = float(config['red']['TIMEOUT'])
FILTRADOS = config['archivos']['FILTRADOS']
COLOR = config['personalizacion']['COLOR']
ESCAN_TIMEOUT = int(config['red']['TIEMPO_DE_ESCANER'])

