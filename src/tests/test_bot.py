import clases.bot
import clases.mcserver
import utilidades.consola



def crear_test_veredicto(estado : int,respuesta_str : str = ''):

    bot = clases.bot.Bot(ip='test')
    bot.numero_estado = estado
    bot.respuesta_str = respuesta_str
    server = clases.mcserver.McServer(ip='test')

    clases.bot.obtener_veredicto(bot,server)

    return (server.veredicto,server.whitelist,server.modeado,server.crackeado)


class TestVeredicto:


    def test_veredicto_pid0(self):

        desconexion = crear_test_veredicto(0)
        assert desconexion[0] == utilidades.consola.ET_IND
        
        for x in range(1,4):
            assert desconexion[x] is False
        

        modeados = ('mods',
                    'FORGE',
                    'MODS',''
                    'FORGE',
                    'this server has mods ...')
        
        for test in modeados:
            mods = crear_test_veredicto(0,test)
            assert mods[0] == utilidades.consola.ET_MOD
            assert mods[1] is False # whitelist
            assert mods[2] is True # modeado
            assert mods[3] is False # no premium
        


        whitelists = (
            'whitelist',
            'You are not whitelisted on this server!',
            'white-listed',
            'WHITELIST',
            'WHITELISTED'
        )

        for test in whitelists:
            whitelist = crear_test_veredicto(0,test)
            assert whitelist[0] == utilidades.consola.ET_CRACK
            assert whitelist[1] is True
            assert whitelist[2] is False
            assert whitelist[3] is True


        baneo = ('BANNED',
                 'banned',
                 'You are banned from this server!')

        for test in baneo:

            ban = crear_test_veredicto(0,test)

            assert ban[0] == utilidades.consola.ET_BAN

            for x in range(1,4):
                assert ban[x] is False
            


    def test_veredicto_pid1(self):

        premium = crear_test_veredicto(1)
        
        assert premium[0] == utilidades.consola.ET_PREM 

        for x in range(1,4):
            assert premium[x] is False

        # caso extra
        premium2 = crear_test_veredicto(1,'test')
        assert premium2[0] == utilidades.consola.ET_PREM 

        for x in range(1,4):
            assert premium2[x] is False


      
    def test_veredicvto_pid3(self):

        crack = crear_test_veredicto(3)
        assert crack[0] == utilidades.consola.ET_CRACK
        assert crack[1] is False
        assert crack[2] is False
        assert crack[3] is True