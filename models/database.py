#Definicao do schema Relacional

db.define_table("Cliente",
			    Field("usu_id","reference auth_user",unique=True,notnull=True,label= "Usuario"),
			    Field("nascimento","date",notnull=True,label = "Data de nascimento"),
			    Field("sexo","string",length = 10,label = "Sexo"),
			    Field("profissao","string",length = 50,label = "Profissão"),
			    format = "%(usu_id.first_name)s"
			   )

db.define_table("Organizacao",
				Field("usu_id","reference auth_user",unique=True,notnull=True,label= "Usuario"),
				Field("eventos","integer",default = 0,label = "Eventos realizados"),
				Field("descricao","text",notnull=True,length = 1000,label = "Descrição"),
				Field("site","string",length = 30,label = "Site"),
				format = "%(usu_id.first_name)s"
			   )

db.define_table("Estabelecimento",
				Field("nome","string",notnull=True,length = 30,label="Nome"),
				Field("cep","string",notnull=True,unique=True,length = 8,label ="CEP"),
				Field("pais","string",notnull=True,length = 30,label ="Pais"),
				Field("estado","string",notnull=True,length = 3,label="Estado(sigla)"),
				Field("cidade","string",notnull=True,length = 30,label="Cidade"),
				format = "%(nome)s"
			   )

db.define_table("Evento",
				Field("org_id", "reference Organizacao",notnull=True,label="Organização"),
				Field("est_id", "reference Estabelecimento",notnull=True,label = "Estabelecimento"),
				Field("img","upload",label="Imagem"),
				Field("titulo","string",notnull=True,length = 50,label="Titulo"),
				Field("descricao","text",length = 1000,label="Descrição"),
				Field("participantes","integer",default = 0,label= "Participantes"),
				auth.signature,
				format = "%(titulo)s"
			   )

db.define_table("Periodo",
				Field("inicio","datetime",notnull=True,label = "Inicio"),
				Field("fim","datetime",notnull=True,label = "Termino"),
				Field("eve_id","reference Evento",notnull=True,label = "Evento")
				)

db.define_table("Participacao",
				Field("cli_id","reference Cliente",notnull=True,label = "Usuario"),
				Field("eve_id","reference Evento",notnull=True,label= "Evento"),
				Field("avaliacao","decimal(3,1)",default = 0.0,label = "Avaliação"),
				Field("avaliou","boolean",default=False,label="Avaliou")
				)

db.define_table("Lote",
				Field("eve_id","reference Evento",notnull=True,label="Evento"),
				Field("preco","double",notnull=True,default = 0.0,label="Preço"),
				Field("total","integer",notnull=True,label="Total"),
				Field("quantidade","integer",compute = lambda L: L["total"]),
				auth.signature
				)

db.define_table("Ticket",
				Field("cli_id","reference Cliente",notnull=True,label="Usuario"),
				Field("lot_id","reference Lote",notnull=True,label ="Lote"),
				auth.signature
				)

db.define_table("Org_Est",
				Field("org_id","reference Organizacao",notnull=True,label = "Organizacao"),
				Field("est_id","reference Estabelecimento",notnull=True,label="Estabelecimento"),
				)

db.define_table("Tag",
				Field("tag","string",notnull=True,length = 30,label="Tag"),
				auth.signature,
				format = "%(tag)s"
				)

db.define_table("Tag_Evento",
				Field("tag_id","reference Tag",length = 30,label="Tag"),
				Field("eve_id","reference Evento",notnull=True,label="Evento"),
				Field("tag","string",notnull=True,length = 30,label="Tag")
				)
				
db.commit()
auth.enable_record_versioning(db)


