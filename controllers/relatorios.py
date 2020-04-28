#Relatorios
def clientes():
	form = SQLFORM.factory(Field("Cliente","integer",requires = IS_IN_DB(db,"Cliente.id")))
	msg = "Relatorios de Cliente"
	if(form.process().accepted):
		cli_id = str(form.vars.Cliente)
		count = db.executesql('SELECT Evento.id, sum( Participacao.avaliacao)/count( Participacao.id) FROM Participacao, Evento WHERE Participacao.cli_id = '+cli_id+' and Participacao.eve_id = Evento.id GROUP BY Evento.id')

		return dict(msg=msg,grid=count) 

	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid = form)


def tag():
	msg = "Relatorio Tag"

	form = SQLFORM.factory(Field("tag",requires = IS_IN_DB(db,"Tag.tag","%(tag)s")))
   
	if(form.process().accepted):
		tag = form.vars.tag
		info = db((db.Tag.tag == tag) & (db.Tag_Evento.tag_id==db.Tag.id) & (db.Tag_Evento.eve_id == db.Participacao.eve_id) & (db.Tag_Evento.eve_id == db.Evento.id)).select( db.Evento.org_id.with_alias('id_organizacao'), db.Evento.id.count(distinct=True).with_alias('numero_de_eventos'), (db.Participacao.id.count(distinct=True)/db.Tag_Evento.eve_id.count(distinct=True)).with_alias('media_de_clientes_pagantes'), groupby=db.Evento.org_id, orderby=db.Evento.org_id , distinct=True)

		return dict(msg=msg,grid=info)

	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)


def tag2():
	form = SQLFORM.factory(Field("tag",requires = IS_IN_DB(db,"Tag.tag","%(tag)s")))
	
	msg = "Relatorio Tag"
	if(form.process().accepted):
		tag = db(db.Tag.tag == form.vars.tag).select().first()
		query = db.Evento.id == db.Tag_Evento.eve_id and tag.id == db.Tag_Evento.tag_id
		rows = db(query).select(db.Tag_Evento.eve_id,db.Tag_Evento.tag_id,db.Evento.participantes,
		join=db.Evento.on(db.Evento.id == db.Tag_Evento.eve_id),groupby=db.Evento.org_id)
	
		return dict(msg=msg,grid=rows)
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)

def intervalos( rows):
#retorna uma lista com cada numero de eventos por numero de lotes do evento
    same = False
    last = rows[0]['contagem'] or None
    contagens = []
    count = 0
    for i in rows:
        if( last == i['contagem']):
            count+=1
        else:
            contagens.append( 'Eventos com numero de lotes igual a '+str(last)+' :'+str(count))
            count=1
        last = i['contagem']
    contagens.append( 'Eventos com numero de lotes igual a '+str(last)+' :'+str(count))
    return contagens

#importe
import datetime
#controlador
def intervalo():
	msg = "Relatorio Intervalos"
	form = SQLFORM.factory(Field("inicio","date",requires=IS_DATE()),
						   Field("fim","date",requires=IS_DATE()))
	
	if(form.process().accepted):
		low = form.vars.inicio
		high = form.vars.fim
		info = db( (db.Evento.id == db.Periodo.eve_id) & (db.Lote.eve_id == db.Evento.id) & (db.Periodo.inicio > low) & (db.Periodo.fim < high)).select( db.Evento.id.with_alias('id_evento'), db.Lote.id.count().with_alias('contagem'), groupby=db.Evento.id, orderby='contagem')
		result = [[]]
		if(info):
			result = intervalos( info)
		return dict(msg=msg,grid=result)

	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)
