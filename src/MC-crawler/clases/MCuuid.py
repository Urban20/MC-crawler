import hashlib
import uuid as UUID



def uuidV4(uuid : str):
   'retorna True si el uuid es de version 4'

   try:
       
       return UUID.UUID(uuid).version == 4
   

   except ValueError:  return False
    

def jugador_crackeado(usuario :str, uuid : str):
    '''
    comprueba si el usuario coincide con el uuid proporcionado cuando es no premium/crackeado
    - usuario : usuario a comprobar
    - uuid : uuid a verificar con el usuario
    
    '''

    return uuid == uuid_Offline(usuario)


def uuid_Offline(usuario : str, string :bool = True):
    'obtiene el uuid offline de un jugador por el algoritmo que utiliza minecraft'
    payload = f'OfflinePlayer:{usuario}'
    version_uuid = 3

    hash = hashlib.md5()
    hash.update(payload.encode())
    hash_md5 = hash.hexdigest()
    uuid_ = UUID.UUID(hex=hash_md5,version=version_uuid)
    
    if string:
        return str(uuid_)
    
    return uuid_
