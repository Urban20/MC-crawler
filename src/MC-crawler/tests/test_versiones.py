from clases.bot import versionado_viejo, versionado_nuevo,v19,v20


class TestVersiones:

    def test_versionado_viejo(self):

        aciertos = (
            '1.20',
            '1.21.10',
            'Paper 1.21.11',
            '1.20.1',
            '1.7'
        )

        for test in aciertos:
            assert versionado_viejo(test) is True
        
        assert versionado_viejo('26.1') is False

        Nones = (
            'test',
            '1.',
            '1.20.20.5',
            'test.test'
        )

        for test in Nones:
            assert versionado_viejo(test) is None
        
    def test_versionado_nuevo(self):

        aciertos = (
            '27.0.0',
            '27.1',
            '28.1.0',
            '26.1',
            'Paper 26.0.0',
            '26.1 Snapshot 11',
            '26.1 Pre-Release 1',
            'v26.1'
        )

        for test in aciertos:
            assert versionado_nuevo(test) is True
        
        fallas = (
            'test',
            '1.20.1',
            'test.test',
            '1.20.20.5',
            '',
            '26'
        )
        for test in fallas:
            assert versionado_nuevo(test) is False
        
    def test_V19(self):

        aciertos = (
            '1.19.2',
            '1.19.1',
            'Paper 1.19.1',
            'Paper 1.19.2'
        )
        
        for test in aciertos:
            assert v19.search(test) is not None 
        
        
        fallas = (
            '1.19.10',
            '1.19.1.8',
            '1.19.',
            '1.19.20'
            '1.19',
            '1.19.3',
            '1.19.0'
        )

        # variantes no validas
        for test in fallas:
            assert v19.search(test) is None
        
        
    def test_V20(self):

        aciertos = (
            '1.20',
            '1.20.1',
            'Paper 1.20.1',
            'Paper 1.20'
        )

        for test in aciertos:
            assert v20.search(test) is not None
        
        # variantes no validas
        Nones = (
            '1.20.10',
            '1.20.',
            '1.20.11',
            '1.200'
            '1.20.1.1'
        )

        for test in Nones:
            assert v20.search(test) is None
        
        
'''
assert v19.search('1.19.2 test') is not None  
assert v19.search('1.19.1 test') is not None
assert v20.search('1.20 test') is not None

POR AHORA NO LAS VOY A TENER EN CUENTA (casos muy aislados)
'''