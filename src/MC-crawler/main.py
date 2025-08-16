from ui import empaquetar
from db import conec




if __name__ == '__main__':
    try:
        empaquetar()
        conec.close()
    except Exception as e:
        print(f'\nhubo un problema: {e}')