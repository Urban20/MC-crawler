from cidr_.escan_flex import es_cidr


def test_cidrs16():


    aciertos = (
        '192.168.0.0/16',
        '50.20.0.0/16',
        '255.168.0.0/16',
        '192.255.0.0/16',
        '255.255.0.0/16'
    )

    for test in aciertos:
        assert es_cidr(test) is True
    
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
        assert es_cidr(test) is False
    

def test_cidr24():


    aciertos = (
        '192.168.0.0/24',
        '50.20.22.0/24',
        '50.0.0.0/24',
    )    

    for test in aciertos:
        assert es_cidr(test,octetos=3) is True

    fallas = (
        '-192.168.0.0/24',
        'test 192.168.0.0/24 test',
        '50.test.0.0/24',
        'test 50.20.1.0/24',
        '50.20.1.0/24 test'
    )

    for test in fallas:
        assert es_cidr(test,octetos=3) is False

def test_es_cidr():

    assert es_cidr('',octetos=5) is False
    assert es_cidr('') is False


    assert es_cidr('192.168.0.0/16',octetos=5) is False
    assert es_cidr('192.168.0.0/24',octetos=2) is False