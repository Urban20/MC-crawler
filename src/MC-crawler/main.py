from ui import empaquetar
from db import conec
import consola

# AUTOR: Urb@n - Matias Urbaneja
# USO RESPONSABLE: Este programa realiza escaneos de direcciones IP y puede generar tráfico elevado.
# RECOMIENDO NO ABUSAR DE LOS ESCANEOS.
# NOTA : El antivirus puede bloquear el funcionamiento o marcarlo como falso positivo.



if __name__ == '__main__': 
    try:
        print(consola.LOGO)
        print(consola.ADVERTENCIA)
        empaquetar()
        conec.close()            
    except Exception as e:
        print(f'\nhubo un problema: {e}')