@auth.requires_login()
@auth.requires_membership("usuario")
def comprar():
	msg = "Comprar Ticket para Evento"

	form = SQLFORM.factory(Field("CPF"),
		    Field("Cartao"),Field("Numero"),
			Field("Senha","password"),
			Field("eve_id","integer",writable=False),
			Field("cli_id","integer",writable=False))

	eve_id = request.args(0, cast=int, otherwise=(URL('evento','default','home')))
	form.vars.eve_id = eve_id

	Cli = db(db.Cliente.usu_id == session.auth.user.id).select().first()
	form.vars.cli_id = Cli.id

	if form.process(onvalidation = valida).accepted:		
		session.flash = 'Compra realizada!'

		##insere na relacao participacao e atualiza os participantes
		pid = db.Participacao.insert(cli_id=Cli.id , eve_id= eve_id)
		db.commit()
		
		##atualiza o numer de participantes do evento
		row = db(db.Evento.id == eve_id).select(db.Evento.id,db.Evento.participantes).first()
		row.participantes = row.participantes + 1
		row.update_record()

		#insere na relacao ticket e atualiza a quantidade de tickets do lote
		Lote = db(db.Lote.eve_id == eve_id and db.Lote.quantidade > 0).select().first()
		pid = db.Ticket.insert(cli_id=Cli.id,lot_id=Lote.id)

		Lote.quantidade = Lote.quantidade - 1
		Lote.update_record()

		redirect(URL('evento','default','meus_eventos'))
	elif form.errors:
		response.flash = 'Erros no formulário ou Cliente ja possui Cadastro!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,form=form)

@auth.requires_login()
@auth.requires_membership("usuario")
def cliente():
	msg = "Cliente"

	db.Cliente.id.readable = db.Cliente.usu_id.writable = False
	Cli = db(db.Cliente.usu_id == session.auth.user.id).select().first()
	form = SQLFORM(db.Cliente,Cli.id)
	
	return dict(msg=msg,grid=form.process())


##verifica se ja existe a relacao cliente - evento
## e veriica se o evento ainda tem lotes disponiveis
def valida(form):
	rows = db(db.Participacao).select(db.Participacao.cli_id,db.Participacao.eve_id)
	lista = rows.as_list()
	tupla = {"cli_id":form.vars.cli_id,"eve_id":form.vars.eve_id}
	if(tupla in lista):
		form.errors.cli_id = "Cliente ja cadastrado"

	Lote = 	db((db.Lote.eve_id == form.vars.eve_id) and (db.Lote.quantidade > 0)).select().first()
	if(Lote == None):
		form.errors.eve_id = "Evento Invalido"