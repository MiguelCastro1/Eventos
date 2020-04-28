#validacoes sobre as Tabelas

db.Cliente.usu_id.requires = [IS_IN_DB(db,"auth_user.id"),IS_NOT_IN_DB(db,"Cliente.id")]
db.Cliente.nascimento.requires = IS_NOT_EMPTY()
db.Cliente.sexo.requires = IS_IN_SET(['Masculino','Feminino','Outro'],zero=None)
db.Cliente.sexo.widget = SQLFORM.widgets.radio.widget
db.Cliente.nascimento.requires = IS_DATE()


db.Organizacao.usu_id.requires = [IS_IN_DB(db,"auth_user.id"),IS_NOT_IN_DB(db,"Organizacao.id")]
db.Organizacao.descricao.requires = IS_NOT_EMPTY()

db.Estabelecimento.nome.requires = IS_NOT_EMPTY()
db.Estabelecimento.cep.requires = IS_NOT_EMPTY()
db.Estabelecimento.cep.requires = IS_NOT_IN_DB(db,"Estabelecimento.cep")
db.Estabelecimento.pais.requires = IS_NOT_EMPTY()
db.Estabelecimento.estado.requires = IS_NOT_EMPTY()
db.Estabelecimento.cidade.requires = IS_NOT_EMPTY()
db.Estabelecimento.id.readable = False

db.Evento.org_id.requires = IS_IN_DB(db,"Organizacao.id")
db.Evento.est_id.requires = IS_IN_DB(db,"Estabelecimento.id","%(nome)s")
db.Evento.titulo.requires = IS_NOT_EMPTY()
db.Evento.img.requires = IS_EMPTY_OR(IS_IMAGE())
db.Evento.id.readable = False

db.Periodo.eve_id.requires = IS_IN_DB(db,"Evento.id","%(titulo)s")
db.Periodo.inicio.requires = IS_NOT_EMPTY()
db.Periodo.fim.requires = IS_NOT_EMPTY()
db.Periodo.fim.requires = IS_DATETIME()
db.Periodo.inicio.requires = IS_DATETIME()
db.Periodo.id.readable = False

db.Participacao.cli_id.requires = IS_IN_DB(db,"Cliente.id")
db.Participacao.eve_id.requires = IS_IN_DB(db,"Evento.id","%(titulo)s")
db.Participacao._plural = "Participacoes"
db.Participacao.id.readable = False

db.Lote.eve_id.requires = IS_IN_DB(db,"Evento.id","%(titulo)s")
db.Lote.preco.requires = IS_NOT_EMPTY()
db.Lote.total.requires = IS_NOT_EMPTY()
db.Lote.id.readable = False

db.Ticket.cli_id.requires = IS_IN_DB(db,"Cliente.id")
db.Ticket.lot_id.requires = IS_IN_DB(db,"Lote.id")
db.Ticket.id.readable = False

db.Org_Est.org_id.requires = IS_IN_DB(db,"Organizacao.id")
db.Org_Est.est_id.requires = IS_IN_DB(db,"Estabelecimento.id")
db.Org_Est.readable = False

db.Tag.tag.requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,"Tag.tag")]
db.Tag.id.readable = False

db.Tag_Evento.eve_id.requires = IS_IN_DB(db,"Evento.id","%(titulo)s")
db.Tag_Evento.tag_id.requires = IS_IN_DB(db,"Tag.id","%(tag)s")
db.Tag_Evento.id.readable = db.Tag_Evento.tag.readable = False

