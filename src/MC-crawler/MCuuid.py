import hashlib
import uuid

def uuid_Offline(usuario : str, string :bool = True):
    'obtiene el uuid offline de un jugador por el algoritmo que utiliza minecraft'
    payload = f'OfflinePlayer:{usuario}'
    version_uuid = 3

    hash = hashlib.md5()
    hash.update(payload.encode())
    hash_md5 = hash.hexdigest()
    uuid_ = uuid.UUID(hex=hash_md5,version=version_uuid)
    if string:
        return str(uuid_)
    else:
        return uuid_
