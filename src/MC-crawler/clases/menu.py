'modulo encargado del menu del programa'


from escaner.gopython import ejecutar_barrido,interrupcion
from db import db
from rich.panel import Panel
from rich import print
from utilidades import consola
from servers import iniciar_busqueda
from utilidades import conectividad
from configuracion import configuracion
import cidr_.escan_flex



class Menu():
    def __init__(self):
        self.titulo = 'OPCIONES'
        self.ejecutando = True
        self.color = configuracion.COLOR
        self.msgcontinuar = 'ENTER para continuar'
        self.delay_input = 0.05


    def __agregar_opcion(self,*args : str):
        t = '\n'
        i = 0
        for desc in args:
            t+= f'{str(i)} → {desc.capitalize()}\n'
            i+=1
        return t
    
    def __panel(self):
        msg = self.__agregar_opcion(
                           'iniciar escaneo de sevidores',
                           'purgar servidores',
                           'buscar POSIBLES servers crackeados',
                           'buscar version (premiums y no premiums)',
                           'ver configuración',
                           'escanear rango personalizado',
                           'salir del programa')

        return Panel(msg,
                      title=self.titulo,
                      border_style=self.color)


    def iniciar(self):

           
        while self.ejecutando:
            consola.limpiar()
            print(self.__panel())

            fecha = db.ultimo_escaneo()
            print(f'Ultimo escaneo registrado: {fecha}\n')

            opcion = consola.input2('[#] seleccionar opcion numero >> ',delay=self.delay_input).strip()
            
            match opcion:
                case '0':
                    if not conectividad.conectividad():
                        continue
                    
                    ejecutar_barrido()
                    
                case '1':
                    if not conectividad.conectividad():
                        continue
                    
                    db.purgar()
                    
                case '2':
                    if not conectividad.conectividad():
                        continue
                    version = iniciar_busqueda(crackeados=True)
                    if version == '0':
                        continue
                    db.buscar_crackeados(version)
                    
                case '3':
                    version = iniciar_busqueda()
                    if version == '0':
                        continue
                    db.buscar_version(version=version)
                    
                case '4':
                    consola.ver_config()
                
                case '5':
                    info = Panel('escaneos de 16 o 24 bits\nejemplos:\n\n190.60.0.0/16\n190.60.20.0/24',
                                 title='uso')
                    print(info)           
                    cidr = str(consola.input2('\nrango a escanear >> ')).strip()
                    cidr_.escan_flex.procesar_rango(cidr)
                case '6':
                    self.ejecutando = False
                    
                case _:
            
                    continue
            
            if self.ejecutando:
                interrupcion.cancelado = False
                input(consola.margen + self.msgcontinuar)

