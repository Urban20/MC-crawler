import subprocess
from escaner.gopython import ruta


def comprobar_escaner(version : str):
    '''
    funcion que verifica si el binario que usa el programa es el adecuado
    
    - version: version que debe coincidir con el binario'''

    sp = subprocess.run([ruta,'-v',],
                        capture_output=True,
                        text=True)
                        
    if sp.returncode != 0:
        return False
    
    return sp.stdout.strip() == version