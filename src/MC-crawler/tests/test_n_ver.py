from clases.bot import n_ver


def test_nver():

    # testeo los casos mas comunes
    assert n_ver('1.20') == 20
    assert n_ver('Paper 1.20') == 20
    assert n_ver('Paper 1.20.5') == 20
    assert n_ver('1.21.5') == 21
    assert n_ver('1.5.2') == 5
    assert n_ver('1.7-') == 7
    assert n_ver('Paper 1.20.x') == 20
    assert n_ver('1.8.x-1.21.x') == 8
    assert n_ver('Velocity 1.7.2-1.21.11') == 7
    
    
    fallas = ( # casos basicos y bastante triviales
        'test',
        '1.test',
        '26.1',
        '26.1.1',
        '27.1'
    )

    for test in fallas:
        assert n_ver(test) is None
    
