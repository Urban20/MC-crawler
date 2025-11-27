'''escaneos personalizados: maneja la logica de parametros introducidos por el usuario'''
from escaner.gopython import introducir_parametros,regex16,regex24
import re



def procesar_rango(cidr : str):
    '''esta funcion precesa rangos cidr de 16 o 24 bits usando la siguiente notacion:
    
    ejemplo:
    
    190.60.0.0/16

    190.60.20.0/24''' 

    cidr16 = re.match(regex16,cidr)
    cidr24 = re.match(regex24,cidr)

    if cidr16:
        print('\niniciando escaneo de 16 bits\n')
        param1 = int(cidr16.group(1))
        param2 = int(cidr16.group(2))
        introducir_parametros(param1=param1,param2=param2)
    elif cidr24:
        print('\niniciando escaneo de 24 bits\n')
        param1 = int(cidr24.group(1))
        param2 = int(cidr24.group(2))
        param3 = int(cidr24.group(3))
        introducir_parametros(param1=param1,param2=param2,param3=param3)

    else:
        print('\nla notacion es invalida\n')
