import datetime

def tiempo_actual():

    'retorna el tiempo actual'

    return datetime.datetime.today().isoformat(sep=' ',timespec='seconds')