'modulo encargado de la UI del programa'

import customtkinter
from servers import Buscar_Servers
from gopython import ejecutar_barrido
from db import buscar_version,buscar_pais,purgar

titulo = 'MC Crawler'
dimension = '500x400'
color_boton = '#3A07AB'
BLANCO = '#FFFFFF'

class UI():
    'la clase UI es la encargada de manejar la interfaz grafica'
    def __init__(self,dimensiones :str ,titulo :str):
        self.dimension = dimensiones
        self.titulo = titulo
        self.pantalla = customtkinter.CTk()

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


def empaquetar():
    'esta funcion contiene TODOS los elementos de la interfaz grafica'
    ui = UI(dimension,titulo)
    pantalla = ui.crear_pantalla()
    # menu de rastreos
    ui.agregar_etiqueta('Rastrear servers por crawling:',13)
    ui.crear_boton('Buscar servidores',Buscar_Servers)
    ui.agregar_etiqueta('Rastrear servers por barridos:',13)
    ui.crear_boton('barrido',ejecutar_barrido)
    ui.agregar_etiqueta('Purgar servers inactivos:',13)
    ui.crear_boton('purgar',purgar)
    # menu de rastreos

    # busquedas - inputs
    ui.agregar_etiqueta('buscar server por version: ',13)
    salida = ui.crear_input()
    ui.crear_boton('buscar version',lambda : buscar_version(salida.get()))
    ui.agregar_etiqueta('buscar server por pais: ',13)
    salida2 = ui.crear_input()
    ui.crear_boton('buscar pais',lambda : buscar_pais(salida2.get()))
   
    pantalla.mainloop()
    