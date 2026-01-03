from clases.menu import Menu
from db import db
import utilidades.consola
from escaner.binario.bin_script import descargar_exe

# AUTOR: Urb@n - Matias Urbaneja
# USO RESPONSABLE: Este programa realiza escaneos de direcciones IP y puede generar tráfico elevado.
# RECOMIENDO NO ABUSAR DE LOS ESCANEOS.
# NOTA : El antivirus puede bloquear el funcionamiento o marcarlo como falso positivo.



if __name__ == '__main__': 
    try:
        utilidades.consola.limpiar()
        descargar_exe()
        menu = Menu()
        menu.iniciar()
        db.conec.close()  
    except KeyboardInterrupt:

        print('\n\nsaliendo del programa\n')        
          
    except Exception as e:
        print(f'\nhubo un problema: {e}')