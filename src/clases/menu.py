'modulo encargado del menu del programa'


from escaner.gopython import ejecutar_barrido,interrupcion
from db import db
from rich.panel import Panel
from rich import print as pr
from utilidades import consola
from servers import iniciar_busqueda
from utilidades import conectividad
import cidr_.escan_flex

class Menu():
    def __init__(self):
        self.titulo = 'OPCIONES'
        self.ejecutando = True
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
                           'iniciar escaneo de servidores',
                           'purgar servidores',
                           'buscar POSIBLES servers crackeados',
                           'buscar version (premiums y no premiums)',
                           'ver configuración',
                           'escanear rango personalizado',
                           'salir del programa')

        consola.box(msg.splitlines())

    def iniciar(self):

           
        while self.ejecutando:
            consola.limpiar()
            consola.imprimir_logo()
            consola.print_centro(f'{' '* len(consola.AMARILLO)}{consola.AMARILLO}(!) Este programa necesita conexion para funcionar correctamente{consola.RESET}')
            self.__panel()

            fecha = db.ultimo_escaneo()
            pr(f'{consola.margen}Ultimo escaneo registrado: {fecha}')
            print('\n')
            opcion = consola.input2(f'{consola.margen}[#] seleccionar opcion numero >> ',delay=self.delay_input).strip()
            

            if not conectividad.conectividad():
                continue
                    
            match opcion:
                case '0':
                    
                    ejecutar_barrido()
                    
                case '1':
                    
                    
                    db.purgar()
                    
                case '2':
                    
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
                    info = Panel('escaneos de 16 , 24 u 8 bits\nejemplos:\n\n190.60.0.0/16\n190.60.20.0/24\n190.0.0.0/8',
                                 title='uso')
                    
                    pr(info)
           
                    cidr = str(consola.input2('\nrango a escanear >> ')).strip()
                    cidr_.escan_flex.procesar_rango(cidr)

                case '6':
                    self.ejecutando = False
                    
                case _:
            
                    continue
            
            if self.ejecutando:
                interrupcion.cancelado = False
                input(consola.margen + self.msgcontinuar)

