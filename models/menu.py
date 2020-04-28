# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('evento','default', 'home'), []),
    (T('Procurar Tags'), False, URL('evento','default', 'procura_tags'), []),
    (T('Meus Eventos'), False, URL('evento','default', 'meus_eventos'), []),
    (T('Criar Evento'), False, URL('evento','organizacao', 'cadastro_evento'), []),
    (T('Meus Perfil'), False, URL(), [
        (T('Usuario'), False, URL('evento','default', 'user',args=['profile']), []),
   		(T('Cliete'), False, URL('evento','usuario', 'cliente'), []),
   		(T('Organizacao'), False, URL('evento','organizacao', 'organizacao'), [])
    	]),

    
    (T('Relatorios'), False, URL(),[
    	(T('Relatorio Tags'), False, URL('evento','default', 'tag'), []),
    	(T('Relatorio Clientes'), False, URL('evento','default', 'clientes'), []),
    	(T('Relatorio Intervalos'), False, URL('evento','default', 'intervalo'), [])
    	])
]

