from peewee import *
import datetime, os
from playhouse.db_url import connect
print(os.environ.get('SCALINGO_MYSQL_URL'))
db = connect(os.environ.get('SCALINGO_MYSQL_URL'))

class Clientes(Model):
    ID= PrimaryKeyField()
    cod_cli = TextField()
    nome = TextField()
    cnpj = TextField()
    ie = TextField()
    endereco = TextField()
    cidade = TextField()
    estado = TextField()
    cep = TextField()
    telefone = TextField()
    fax = TextField()
    email = TextField()
    obs = TextField()
    class Meta:
        db_table = 'Clientes'
        database = db


class Cadastro_OS(Model):
    Id = PrimaryKeyField()
    Tipo = TextField()
    Numero_Os = IntegerField()
    Id_Cliente = IntegerField()
    Data = DateTimeField(default=datetime.datetime.now)
    Prazo = DateTimeField()
    gravacao = TextField()
    Ferramenta = TextField()
    Material = TextField()
    Especificacao = TextField()
    Quantidade = IntegerField()
    unidade = TextField()
    Desenho_Cliente = TextField()
    Desenho_Pimentel = TextField()
    Numero_Nf = IntegerField()
    Numero_Pedido = IntegerField()
    Data_Nf = DateTimeField()
    Data_Pedido = DateTimeField()
    STATUS = TextField()
    gravacao2 = TextField()
    class Meta:
        db_table = 'Cadastro_OS'
        database = db

class Estoque(Model):
    ID = PrimaryKeyField()
    id_cliente = IntegerField()
    ferramenta = TextField()
    material = TextField()
    cod_pc = TextField()
    mm = TextField()
    qt = IntegerField()
    gaveta = IntegerField()
    data = DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = 'Estoque'
        database = db
class usuarios(Model):
    ID = PrimaryKeyField()
    ds_senha = TextField()
    ds_login = TextField()
    nivel = IntegerField()
    desc = TextField()
    class Meta: 
        db_table = 'usuarios'
        database = db

class contasapagar(Model):
    ID = PrimaryKeyField()
    vencimento = TextField()
    descricao = TextField()
    cod_fornecedor = IntegerField()
    valor = FloatField()
    pago = IntegerField()
    data_pagamento = TextField()
    class Meta: 
        db_table = 'contasapagar'
        database = db

class orcamento(Model):
    ID = PrimaryKeyField()
    numero = IntegerField()
    ano = IntegerField()
    cod_item = IntegerField()
    data = DateTimeField(default=datetime.datetime.now)
    attn = TextField()
    refer = TextField()
    de = TextField()
    nref = TextField()
    fax = TextField()
    prazo_entrega = TextField()
    prazo_pagto = TextField()
    ipi = TextField()
    icms = TextField()
    class Meta:
        db_table = 'orcamento' 
        database = db

class caixa(Model):
    id = PrimaryKeyField()
    tipo = TextField()
    descricao = TextField()
    valor = FloatField()
    data = TextField()
    mes  = TextField()
    ano = IntegerField()
    class Meta:
        db_table = 'caixa'
        database = db

class Fornecedores(Model):
    ID = PrimaryKeyField()
    cod_for = TextField()
    nome = TextField()
    cnpj = TextField()
    ie = TextField()
    endereco = TextField()
    cidade = TextField()
    estado = TextField()
    cep = TextField()
    telefone = TextField()
    fax = TextField()
    email = TextField()
    obs = TextField()
    qntcompras = IntegerField()
    class Meta:
        db_table = 'Fornecedores'
        database = db
    
class Ferramenta(Model):
    ID = PrimaryKeyField()
    Ferramenta = TextField()
    Cod_ferramenta = TextField()
    cod_cli = IntegerField()
    mm = IntegerField()

class compras(Model):
    ID = PrimaryKeyField()
    cod_fornecedor = IntegerField()
    data = DateTimeField(default=datetime.datetime.now)
    qnt = IntegerField()
    preco = FloatField()
    desc = TextField()
    ipi = TextField()
    prazo = TextField()
    cond = TextField()
    contato = TextField()
    class Meta:
        db_table = 'compras'
        database = db

class contas_desc(Model):
    id = PrimaryKeyField()
    descx = TextField()

class controle(Model):
    id = PrimaryKeyField()
    cod_item = IntegerField()
    cod_cli = IntegerField()
    gaveta = IntegerField()
    quantidade = IntegerField()
    data = TextField()
    class Meta:
        db_table = 'controle'
        database = db

class Pedidos(Model):
    ID = PrimaryKeyField()
    numero = IntegerField()
    ano = IntegerField()
    id_cliente = IntegerField()
    id_ferramenta = IntegerField()
    especificacao = TextField()
    desenho = TextField()
    unidade = TextField()
    qnt = IntegerField()
    preco = FloatField()
    data_entrada = DateTimeField(default=datetime.datetime.now)
    prazo = DateTimeField()
    qnt_acabada = TextField()
    data_acabamento = DateTimeField()
    pedido_cliente = TextField()
    numero_os = IntegerField()
    status = IntegerField()
    class Meta:
        db_table = 'Pedidos'
        database = db
    
class funcionarios(Model):
    id = PrimaryKeyField()
    funcionario = TextField()
    nome = TextField()
    senha = TextField()
    class Meta:
        db_table = 'funcionarios'
        database = db
    
class ponto(Model):
    id = PrimaryKeyField()
    cod_func = IntegerField()
    data = DateTimeField(default=datetime.datetime.now)
    hora = TextField(default = str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute))
    tipo = TextField()
    class Meta:
        db_table = 'ponto'
        database = db

class Material(Model):
    ID = PrimaryKeyField()
    material = TextField()
    cod_material = TextField()
    class Meta:
        db_table = 'Material'
        database = db

class notafiscal(Model):
    id_nf = PrimaryKeyField()
    numero_nf = IntegerField()
    data_nf= TextField()
    valor_nf = TextField()
    class Meta:
        db_table = 'notafiscal'
        database = db

class processos(Model):
    ID = PrimaryKeyField()
    Nome = TextField()
    Tempo_Objetivo = TextField()
    class Meta:
        db_table = 'processos'
        database = db

class Historico_os(Model):
    ID = PrimaryKeyField()
    id_proc = IntegerField()
    id_os = IntegerField()
    inicio = TextField()
    fim = TextField()
    periodo = IntegerField()
    data = TextField()
    qtd = IntegerField() 
    class Meta:
        db_table = 'Historico_os'
        database = db