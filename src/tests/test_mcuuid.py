from clases.MCuuid import uuid_Offline,uuidV4
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

def test_UuidV4():

    aciertos = ('e54ec9de-013e-4281-bd91-c48def8feb99',
                'f0e665a4-75eb-488d-9f6d-b3c9d04acc9c')

    for test in aciertos:
        assert uuidV4(test) is True
   

    fallas = (
        'e54ec9de-013e-3281-bd91-c48def8feb99',
        '00000000-0000-4000-0000-000000000000',
        'TEST e54ec9de-013e-4281-bd91-c48def8feb99 TEST',
        'test',
    )

    for test in fallas:
        assert uuidV4(test) is False
   
