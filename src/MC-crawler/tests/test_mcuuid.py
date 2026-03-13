from clases.MCuuid import uuid_Offline
from uuid import UUID

class TestMcuuidOffline:

    def test_uuidOffline(self):
        assert uuid_Offline('Steve') == '5627dd98-e6be-3c21-b8a8-e92344183641'
        assert uuid_Offline('Alex') == '36532b5e-c442-3dbb-a24c-c7e55d0f979a'

    def test_distintos(self):

        comparacion = lambda usuario : uuid_Offline(usuario.capitalize()) != uuid_Offline(usuario.lower())
        
        assert comparacion('steve')
        assert comparacion('alex')

    def test_tipos(self):

        assert type(uuid_Offline('test')) is str
        assert type(uuid_Offline('test',string=False)) is UUID