# -*- coding: utf-8 -*-

def index():
	redirect(URL('evento','default','home'))

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

#Pagina Principla que mostra todos os eventos disponiveis
def home():
	db.Evento.created_on.readable = True

	#liks paras as tabelas relacionadas
	links_tables = ['Tag_Evento','Periodo','Lote'] 

	#campo extra de avaliacao(campo virtual) e de compra de ingresso
	links_extra = [dict(header='Avaliacao', body = avaliacao),
				   dict(header='Ingresso', body= lambda row: 
	A("comprar",callback= URL("evento","usuario","comprar",args=[row.id]),target="_self" ))]
	
	form = SQLFORM.smartgrid(db.Evento,deletable=False,linked_tables=links_tables,
	links=links_extra,create=False,csv=False,editable=False,user_signature=False,
	maxtextlength=10)

	return dict(grid=form)

def procura_tags():
	response.view = 'default/home.html'
	
	form = SQLFORM.factory(Field("tag",requires = IS_IN_DB(db,"Tag.tag","%(tag)s")))
	
	if(form.process().accepted):
		pid = db(db.Tag.tag == form.vars.tag).select().first()
		
		links_c = [dict(header='Avaliacao', body = avaliacao),
				   dict(header='Ingresso', body= lambda row: 
		A("comprar",callback=URL("evento","usuario","comprar",args=[row.id]),target="_self" ))]
		
		query = (db.Tag_Evento.eve_id == db.Evento.id) and (db.Tag_Evento.tag_id == pid.id)
		form = SQLFORM.grid(query,deletable=False,links=links_c,create=False,csv=False,editable = False)
		
	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(grid=form)

## mostra os eventos que o usuario comprou
## ou eventos criados pela organizacao
@auth.requires_login()
def meus_eventos():
	msg = "Meus Eventos"

	##Verificar se eh um usuario ou organizacao
	usu = db(db.Cliente.usu_id == session.auth.user.id).select()
	
	if(usu):
		db.Participacao.cli_id.writable = db.Participacao.eve_id.writable = False
		Cli = db(db.Cliente.usu_id == session.auth.user.id).select().first()
		query = (db.Evento.id == db.Participacao.eve_id) and (Cli.id == db.Participacao.cli_id)
		form = SQLFORM.grid(query,deletable=False,create=False,csv=False,user_signature=False)

	else:
		db.Evento.created_on.readable = True
		db.Evento.participantes.writable = db.Evento.org_id.writable = False
		org = db(session.auth.user.id == db.Organizacao.usu_id).select().first()
		query = (db.Evento.org_id == org.id)

		links = [dict(header='Avaliacao', body = avaliacao)]
		form = SQLFORM.grid(query,deletable=False,create=False,csv=False,user_signature=False,links=links)

	return dict(msg=msg,rows=form)

@auth.requires_login()
def registro():
	msg = "Registro de Cliente ou Organizacao"
	
	##impede que o usuario seja de 2 grupos
	if auth.has_membership(2, session.auth.user.id) or auth.has_membership(3, session.auth.user.id):
		redirect(URL('evento','default','home'))

	db.Cliente.usu_id.writable = False
	form1 = SQLFORM(db.Cliente)

	#atribuindo o usu_id igual ao do usuario
	form1.vars.usu_id = session.auth.user.id

	if form1.process().accepted:
		session.flash = 'Cadastro aceito!'
		#inseri no grupo de usuarios
		auth.add_membership(2, session.auth.user.id) 
		redirect(URL('evento','default','home'))
	elif form1.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	db.Organizacao.usu_id.writable = db.Organizacao.eventos.writable = False
	form2 = SQLFORM(db.Organizacao)

	#atribuindo o usu_id igual ao do usuario
	form2.vars.usu_id = session.auth.user.id

	if form2.process().accepted:
		session.flash = 'Formulário aceito!'
		#inseri no grupo de organizacao
		auth.add_membership(3, session.auth.user.id)
		redirect(URL('evento','default','home'))
	elif form2.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,form1=form1,form2=form2)


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

##########Funcoes################

#Calcula a avaliacao(nota) de um evento
def avaliacao(row):
	query = db.Participacao.eve_id == row.id 
	rows = avaliacao = db(query).select(db.Participacao.avaliacao,db.Participacao.avaliou)

	avaliacao = 0
	for row in rows:
		if(row.avaliou): 
			avaliacao += row.avaliacao
	if(len(rows) > 0):
		avaliacao = avaliacao / len(rows)
	return round(avaliacao, 2)

