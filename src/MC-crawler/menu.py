'modulo encargado del menu del programa'


from gopython import ejecutar_barrido
from db import buscar_version,purgar,buscar_crackeados
from rich.panel import Panel
from rich import print
import consola
from servers import conectividad,iniciar_busqueda
import configuracion



class Menu():
    def __init__(self):
        self.titulo = 'opciones'
        self.mensaje = '''
        0: Ejecutar barrido
        1: Purgar servidores
        2: Buscar POSIBLES servers crackeados
        3: Buscar version (premiums y no premiums)
        4: Salir del programa
        5: ver configuración
        '''
        self.ejecutando = True
        self.color = configuracion.COLOR
        self.msgcontinuar = 'ENTER para continuar' 

    def iniciar(self):

        panel = Panel(self.mensaje,title=self.titulo,style=self.color)
        
        while self.ejecutando:
            consola.limpiar()
            print(panel)
            opcion = str(input('[#] seleccionar opcion >> ')).strip()
            
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
                        version = iniciar_busqueda(crackeados=True)
                        buscar_crackeados(version)
                    input(self.msgcontinuar)
                case '3':
                    version = iniciar_busqueda()
                    buscar_version(version=version)
                    input(self.msgcontinuar)
                case '4':
                    self.ejecutando = False
                case '5':
                    consola.ver_config()
                    input(self.msgcontinuar)
                case _:
            
                    continue
                    

