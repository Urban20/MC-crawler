'''escaneos personalizados: maneja la logica de parametros introducidos por el usuario'''
from escaner.gopython import introducir_parametros,interrupcion
import re
import cidr_.data

reg16 = cidr_.data.regex16 + '$'
reg24 = cidr_.data.regex24 + '$'

es_octeto = lambda oct: int(oct) >= 0 and int(oct) <= 255

def es_cidr(cidr : str,octetos = 2): # revisar

    'da True si el reg especificado coincide con un rango'

    if octetos not in (2,3):
        return False

    if octetos == 2:
        regex = reg16
    else:
        regex = reg24

    r = re.match(regex,cidr)

    if r is None:
        return False
    
    for x in range(1,octetos + 1):

        if not es_octeto(r.group(x)):
            return False
        
    return True
    
def procesar_rango(cidr : str):
    '''esta funcion precesa rangos cidr de 16 o 24 bits usando la siguiente notacion:
    
    ejemplo:
    
    190.60.0.0/16

    190.60.20.0/24''' 

    cidr16 = es_cidr(cidr=cidr,octetos=2)
    cidr24 = es_cidr(cidr=cidr)

    if cidr16:
        print('\niniciando escaneo de 16 bits\n')
        interrupcion.iniciar()
        param1 = int(cidr16.group(1))
        param2 = int(cidr16.group(2))
        introducir_parametros(param1=param1,
                              param2=param2)
    elif cidr24:
        print('\niniciando escaneo de 24 bits\n')
        interrupcion.iniciar()
        param1 = int(cidr24.group(1))
        param2 = int(cidr24.group(2))
        param3 = int(cidr24.group(3))
        
        introducir_parametros(param1=param1,
                              param2=param2,
                              param3=param3,
                              bits24=True)

    else:
        print('\nla notacion es invalida\n')
