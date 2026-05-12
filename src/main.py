from clases.menu import Menu
from db import db
import utilidades.consola
from escaner.binario.bin_script import descargar_exe,VERSION_BIN,check_binario_linux
import escaner.binario.verificador
import time
import sys
from colorama import init

'''
AUTOR: Urb@n - Matias Urbaneja
Mc-Crawler : Herramienta de descubrimiento de servidores de Minecraft Java

------------------------------------------------------------------------------
MIT License 

Copyright (c) 2025 Urban20

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


def main():
    delay = 1
    init()
    print(f'\033]2;MC-Crawler {utilidades.consola.VERSION}\007')
    utilidades.consola.limpiar()
    check_binario_linux()
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



if __name__ == '__main__': 
    try:  
        main()
          
    except KeyboardInterrupt:

        print('\n\nsaliendo del programa\n')        
          
    except Exception as e:
        print(f'\nhubo un problema: {e}')