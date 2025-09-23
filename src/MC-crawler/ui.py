'modulo encargado de la UI del programa'

import customtkinter
from servers import Buscar_Servers
from gopython import ejecutar_barrido
from db import buscar_version,buscar_pais,purgar,buscar_crackeados

VERSION = 'V2.3' # version del programa
titulo = 'MC Crawler ' + VERSION
dimension = '500x400'
color_boton = '#3A07AB'
BLANCO = '#FFFFFF'
TAMAÑO_ETIQUETA = 13

class UI():
    'la clase UI es la encargada de manejar la interfaz grafica'
    def __init__(self,dimensiones :str ,titulo :str):
        self.dimension = dimensiones
        self.titulo = titulo
        self.pantalla = customtkinter.CTk()
        self.bloqueada = False # si es True la interfaz ignora al usuario

    def actualizar_estado(self):
        if self.bloqueada:
            estado = 'disabled'
        else:
            estado = 'normal'

        for funcion in self.pantalla.winfo_children():
            funcion.configure(state=estado)

    def crear_input(self):
        entrada = customtkinter.CTkEntry(self.pantalla,fg_color='transparent')
        
        entrada.pack()
        return entrada

    def agregar_etiqueta(self,texto : str,tamaño):
        et = customtkinter.CTkLabel(self.pantalla,text=texto,font=('Arial',tamaño))
        et.pack()
    
    def crear_boton(self,texto : str,funcion):
        boton = customtkinter.CTkButton(self.pantalla,text=texto
                                        ,command=funcion,
                                        fg_color=color_boton,
                                        border_color=BLANCO,
                                        border_width=2,
                                        )
        
        boton.pack()

    def crear_pantalla(self):
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme(color_string='blue')
        self.pantalla.title(self.titulo)
        self.pantalla.geometry(self.dimension)
        
        return self.pantalla

interfaz = UI(dimension,titulo)

def empaquetar():
    'esta funcion contiene TODOS los elementos de la interfaz grafica'
    
    pantalla = interfaz.crear_pantalla()
    # menu de rastreos
    interfaz.agregar_etiqueta('Rastrear servers por crawling:',TAMAÑO_ETIQUETA)
    interfaz.crear_boton('Buscar servidores',Buscar_Servers)
    interfaz.agregar_etiqueta('Rastrear servers por barridos:',TAMAÑO_ETIQUETA)
    interfaz.crear_boton('barrido',ejecutar_barrido)
    interfaz.agregar_etiqueta('Purgar servers inactivos:',TAMAÑO_ETIQUETA)
    interfaz.crear_boton('purgar',purgar)
    interfaz.agregar_etiqueta('buscar posibles servers crackeados',TAMAÑO_ETIQUETA)
    interfaz.crear_boton('buscar',buscar_crackeados)
    # menu de rastreos

    # busquedas - inputs
    interfaz.agregar_etiqueta('buscar server por version: ',TAMAÑO_ETIQUETA)
    salida = interfaz.crear_input()
    interfaz.crear_boton('buscar version',lambda : buscar_version(salida.get()))
    interfaz.agregar_etiqueta('buscar server por pais: ',TAMAÑO_ETIQUETA)
    salida2 = interfaz.crear_input()
    interfaz.crear_boton('buscar pais',lambda : buscar_pais(salida2.get()))
    pantalla.mainloop()
