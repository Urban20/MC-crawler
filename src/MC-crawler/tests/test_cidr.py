from cidr_.escan_flex import es_cidr,es_octeto

class TestCidrs:

    def test_cidrs16(self):


        aciertos = (
            '192.168.0.0/16',
            '50.20.0.0/16',
            '255.168.0.0/16',
            '192.255.0.0/16',
            '255.255.0.0/16'
        )

        for test in aciertos:
            assert es_cidr(test)[0] is True
            assert es_cidr(test)[1] is not None
        
        fallas = (
            'test 192.168.0.0/16',
            '192.168.0.0/16 test',
            'test 192.168.0.0/16 test',
            '700.168.0.0/16',
            '192.168.0.0/160',
            '192.1680.0.0/16',
            '192.168.1.0/16',
            '192.168.0.1/16',
            '192.-168.0.1/16',
            '-25.-168.0.1/16',
            'test.50.0.0/16',
        )

        for test in fallas:
            assert es_cidr(test)[0] is False
            assert es_cidr(test)[1] is None

    def test_cidr24(self):


        aciertos = (
            '192.168.0.0/24',
            '50.20.22.0/24',
            '50.0.0.0/24',
        )    

        for test in aciertos:

            ejecucion = es_cidr(test,octetos=3)
            assert ejecucion[0] is True
            assert ejecucion[1] is not None

        fallas = (
            '-192.168.0.0/24',
            'test 192.168.0.0/24 test',
            '50.test.0.0/24',
            'test 50.20.1.0/24',
            '50.20.1.0/24 test'
        )

        for test in fallas:
            ejecucion = es_cidr(test,octetos=3)
            assert ejecucion[0] is False
            assert ejecucion[1] is None

    def test_es_cidr(self):

        erroneo = es_cidr('',octetos=5)
        assert erroneo[0] is False
        assert erroneo[1] is None

        erroneo = es_cidr('')
        assert erroneo[0] is False
        assert erroneo[1] is None

        erroneo = es_cidr('192.168.0.0/16',octetos=5)
        assert erroneo[0] is False
        assert erroneo[1] is None

        erroneo = es_cidr('192.168.0.0/24',octetos=2)
        assert erroneo[0] is False
        assert erroneo[1] is None

def test_es_octeto():
    assert es_octeto(0) is True
    assert es_octeto(1) is True
    assert es_octeto(255) is True
    assert es_octeto(-2) is False
    assert es_octeto(256) is False