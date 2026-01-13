from clases.menu import Menu
from db import db
import utilidades.consola
from escaner.binario.bin_script import descargar_exe,VERSION_BIN
import escaner.binario.verificador
import time
import sys
from colorama import init


# AUTOR: Urb@n - Matias Urbaneja
# USO RESPONSABLE: Este programa realiza escaneos de direcciones IP y puede generar tráfico elevado.
# RECOMIENDO NO ABUSAR DE LOS ESCANEOS.
# NOTA : El antivirus puede bloquear el funcionamiento o marcarlo como falso positivo.



if __name__ == '__main__': 
    try:
        delay = 1
        init()
        utilidades.consola.limpiar()
        descargar_exe()

        if not escaner.binario.verificador.comprobar_escaner(VERSION_BIN):
            print(f'\nel escaner actual es incompatible con el programa:\nse necesita la version {VERSION_BIN}')
            time.sleep(delay)
            sys.exit(1)

        print(f'\n✓ escaner compatible: {VERSION_BIN}\n')    
        time.sleep(delay)
        menu = Menu()
        menu.iniciar()
        db.conec.close()  
    except KeyboardInterrupt:

        print('\n\nsaliendo del programa\n')        
          
    except Exception as e:
        print(f'\nhubo un problema: {e}')