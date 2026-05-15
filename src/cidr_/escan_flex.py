'''escaneos personalizados: maneja la logica de parametros introducidos por el usuario'''
from escaner.gopython import introducir_parametros,interrupcion
import re
import cidr_.data

reg16 = cidr_.data.regex16 + '$'
reg24 = cidr_.data.regex24 + '$'
reg8 = cidr_.data.regex8+ '$'

es_octeto = lambda oct: int(oct) >= 0 and int(oct) <= 255

def es_cidr(cidr : str,octetos = 2): # revisar

    'da True si el reg especificado coincide con un rango'

    if octetos not in (1,2,3):
        return False, None
    

    match octetos:

        case 1:
            regex = reg8
        case 2:
            regex = reg16
        case _:
            regex = reg24

    r = re.match(regex,cidr)

    if r is None:
        return False, None
    
    for x in range(1,octetos + 1):

        if not es_octeto(r.group(x)):
            return False , None
        
    return True , r
    
def procesar_rango(cidr : str):
    '''esta funcion precesa rangos cidr de 16 o 24 bits usando la siguiente notacion:
    
    ejemplo:
    
    190.60.0.0/16

    190.60.20.0/24''' 

    cidr16,reg = es_cidr(cidr=cidr)
    cidr24,reg2 = es_cidr(cidr=cidr,octetos=3)
    cidr8,reg3 = es_cidr(cidr=cidr,octetos=1)

    if cidr8 and reg3:
        print('\niniciando escaneo de 8 bits\n')
        interrupcion.iniciar()
        param1 = int(reg3.group(1))
        introducir_parametros(param1=param1,bits8=True)

    if cidr16 and reg:
        print('\niniciando escaneo de 16 bits\n')
        interrupcion.iniciar()
        param1 = int(reg.group(1)) 
        param2 = int(reg.group(2))
        introducir_parametros(param1=param1,
                              param2=param2)
    elif cidr24 and reg2:
        print('\niniciando escaneo de 24 bits\n')
        interrupcion.iniciar()
        param1 = int(reg2.group(1))
        param2 = int(reg2.group(2))
        param3 = int(reg2.group(3))
        
        introducir_parametros(param1=param1,
                              param2=param2,
                              param3=param3,
                              bits24=True)

    else:
        print('\nla notacion es invalida\n')
