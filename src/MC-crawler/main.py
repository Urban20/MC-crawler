from menu import Menu
from db import conec
import consola

# AUTOR: Urb@n - Matias Urbaneja
# USO RESPONSABLE: Este programa realiza escaneos de direcciones IP y puede generar tráfico elevado.
# RECOMIENDO NO ABUSAR DE LOS ESCANEOS.
# NOTA : El antivirus puede bloquear el funcionamiento o marcarlo como falso positivo.



if __name__ == '__main__': 
    try:
        consola.limpiar()
        
        menu = Menu()
        menu.iniciar()
        conec.close()  
    except KeyboardInterrupt:

        print('\n\nsaliendo del programa\n')        
          
    except Exception as e:
        print(f'\nhubo un problema: {e}')