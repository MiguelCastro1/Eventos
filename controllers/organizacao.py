
@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_evento():
	msg = "Cadastrar Eventos"
	db.Evento.participantes.writable = db.Evento.org_id.writable = False

	form = SQLFORM(db.Evento,buttons=[BUTTON('cadastrar', _type="submit"),
	A("Cadastrar Estabelecimento", _class='btn-primary', _href=URL('evento','organizacao', 'cadastro_Estabelecimento'))])
    
	Org = db(db.Organizacao.usu_id == session.auth.user.id).select().first()
	form.vars.org_id = Org.id
   
	if form.process().accepted:
		session.flash = 'Cadastro aceito!'
		Org.eventos = Org.eventos + 1
		Org.update_record()
	
		redirect(URL('evento','organizacao',"cadastro_Periodo",args=[form.vars.id]))
	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_Estabelecimento():
    msg = "Cadastrar Estabelecimento"

    form = SQLFORM(db.Estabelecimento)
    if form.process().accepted:
        session.flash = 'Cadastro aceito!'
        redirect(URL('evento','organizacao','cadastro_evento'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_Periodo():
    msg = "Cadastrar Periodo"

    db.Periodo.eve_id.writable = False
    form = SQLFORM(db.Periodo,buttons=[BUTTON('cadastrar', _type="submit"),
	A("Continuar", _class='btn_primary', _href=URL('evento','organizacao','cadastro_Lote',args=[request.args(0)]))])

    form.vars.eve_id = request.args(0, cast=int, otherwise=URL('evento','default','home'))
    if form.process().accepted:
        session.flash = 'Cadastro aceito!'
        redirect(URL('evento','organizacao','cadastro_Lote',args=[form.vars.eve_id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_Lote():
    msg = "Cadastrar Lote"
    db.Lote.eve_id.writable = False
    
    form = SQLFORM(db.Lote)
    form.vars.eve_id = request.args(0, cast=int, otherwise=URL('evento','default','home'))
    if form.process().accepted:
        session.flash = 'Cadastro aceito!'
        redirect(URL('evento','organizacao',"cadastro_Tags",args=[form.vars.eve_id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_Tags():
	msg = "Cadastrar Tags para o Evento"
	db.Tag_Evento.eve_id.writable = db.Tag_Evento.tag.writable = False	

	form = SQLFORM(db.Tag_Evento,buttons=[BUTTON('cadastrar', _type="submit"),
	A("Criar Tag", _class='btn-primary', _href=URL('evento','organizacao',"criar_Tag",args=[request.args(0)])),
	A("Finalizar", _class='btn-primary', _href=URL('evento','default',"meus_eventos"))])

	form.vars.tag = "" #gambiarra
	form.vars.eve_id = request.args(0, cast=int, otherwise=URL('evento','default','home'))

	if form.process().accepted:
		session.flash = 'Cadastro aceito!'
		redirect(URL('evento','organizacao','cadastro_Tags',args=[form.vars.eve_id]))  
	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def criar_Tag():
    msg = "Criar Tag"
    form = SQLFORM(db.Tag)

    if form.process().accepted:
        session.flash = 'Cadastro aceito!'
        redirect(URL('evento','organizacao',"cadastro_Tags",args=[request.args(0)]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def organizacao():
	msg = "Organizacao"
	db.Organizacao.id.readable = False
	db.Organizacao.usu_id.writable = db.Organizacao.eventos.writable = False

	Org = db(db.Organizacao.usu_id == session.auth.user.id).select().first()
	form = SQLFORM(db.Organizacao,Org.id)

	return dict(msg=msg,grid=form.process())

