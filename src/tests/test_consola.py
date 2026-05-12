from utilidades.consola import maximo


def test_maximo():

    assert maximo([]) == 0
    assert maximo(['test']) == 4
    assert maximo(['test','testeando','testeo']) == 9
    