'modulo encargado de la UI del programa'


from gopython import ejecutar_barrido
from db import buscar_version,purgar,buscar_crackeados
from rich.panel import Panel
from rich import print
import consola
from servers import conectividad

class Menu():
    def __init__(self,color_panel = 'medium_purple3'):
        self.titulo = 'opciones'
        self.mensaje = '''
        0: Ejecutar barrido
        1: Purgar servidores
        2: Buscar POSIBLES servers crackeados
        3: Buscar version
        4: Salir del programa
        '''
        self.ejecutando = True
        self.color = color_panel
        self.msgcontinuar = 'ENTER para continuar' 

    def iniciar(self):

        panel = Panel(self.mensaje,title=self.titulo,style=self.color)
        
        while self.ejecutando:
            consola.limpiar()
            print(panel)
            opcion = str(input('[#] seleccionar opcion > ')).strip()
            
            match opcion:
                case '0':
                    if conectividad():
                        ejecutar_barrido()
                    input(self.msgcontinuar)
                case '1':
                    if conectividad():
                        purgar()
                    input(self.msgcontinuar)
                case '2':
                    if conectividad():
                        buscar_crackeados()
                    input(self.msgcontinuar)
                case '3':
                    version = str(input('version > ')).strip()
                    buscar_version(version=version)
                    input(self.msgcontinuar)
                case '4':
                    self.ejecutando = False
                case _:
            
                    continue
                    

