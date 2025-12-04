import configparser
import os


ARCHIVO = 'configuracion.ini' # no modificar
DIR_PY = os.path.dirname(__file__)
DIR = os.path.join(DIR_PY,ARCHIVO)
DOCUMENTACION = r'''
# hilos: hilos en paralelo para el escaner de ipv4s, NO MODIFICAR SIN SABER LO QUE SE ESTA HACIENDO
# timeout : tiempo de espera entre servidores
# filtrados : archivo donde se guardan los servers filtrados al buscar (.txt)
# COLOR : color que utilizara la consola, revisar https://rich.readthedocs.io/en/stable/appendix/colors.html
# TIEMPO_DE_ESCANER : tiempo de espera en milisegundos del escaner de puertos (binario)
'''

config = configparser.ConfigParser()

def generar_ini():

    if os.path.exists(DIR):
        return

    config['red'] = {'hilos': 1500,
                    'timeout':0.6,
                    'tiempo_de_escaner': 700}
    
    config['archivos'] = {'filtrados': 'filtrados.txt'}

    config['personalizacion'] = {'color': 'medium_purple3'}

    with open(DIR,'w') as conf:
        conf.write(DOCUMENTACION)
        config.write(conf)
        

generar_ini()

# lectura del ini 
config.read(DIR)
HILOS = int(config['red']['HILOS'])
TIMEOUT = float(config['red']['TIMEOUT'])
FILTRADOS = config['archivos']['FILTRADOS']
COLOR = config['personalizacion']['COLOR']
ESCAN_TIMEOUT = int(config['red']['TIEMPO_DE_ESCANER'])
