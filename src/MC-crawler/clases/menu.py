'modulo encargado del menu del programa'


from gopython import ejecutar_barrido
from db import buscar_version,purgar,buscar_crackeados
from rich.panel import Panel
from rich import print
from utilidades import consola
from servers import iniciar_busqueda
from utilidades import conectividad
from configuracion import configuracion
import cidr_.escan_flex



class Menu():
    def __init__(self):
        self.titulo = 'opciones'
        self.mensaje = '''
        0: Ejecutar barrido
        1: Purgar servidores
        2: Buscar POSIBLES servers crackeados
        3: Buscar version (premiums y no premiums)
        4: ver configuración
        5: escanear rango personalizado
        6: salir del programa
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
                    if not conectividad.conectividad():
                        continue
                    
                    ejecutar_barrido()
                    
                case '1':
                    if not conectividad.conectividad():
                        continue
                    
                    purgar()
                    
                case '2':
                    if not conectividad.conectividad():
                        continue

                    version = iniciar_busqueda(crackeados=True)
                    buscar_crackeados(version)
                    
                case '3':
                    version = iniciar_busqueda()
                    buscar_version(version=version)
                    
                case '4':
                    consola.ver_config()
                
                case '5':
                    info = Panel('escaneos de 16 o 24 bits\nejemplos:\n\n123.1.0.0/16\n123.123.123.0/24',
                                 title='uso')
                    print(info)           
                    cidr = str(input('\nrango a escanear >> ')).strip()
                    cidr_.escan_flex.procesar_rango16(cidr)
                case '6':
                    self.ejecutando = False
                    
                case _:
            
                    continue

            input(self.msgcontinuar)

