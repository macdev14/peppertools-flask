from peewee import *
import datetime
from os.path import expanduser
home = expanduser("~")
perms = {'key': home+'/ssl/ca.pem', 
         'cert': home+'/ssl/ca.pem', 
         'ca': home+'/ssl/ca.pem',
          'useSSL':True,
         'verifyServerCertificate': False,
        
         }
db = None
while not db:
    db = MySQLDatabase('no5k31nx620ibo35', user='yky1691ysl6jmyiv', passwd='p9roi4nf30ztb4xh', charset='utf8mb4',  host='cis9cbtgerlk68wl.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', port=3306)

class Clientes(Model):
    ID= PrimaryKeyField()
    cnpj = TextField()
    email = TextField()  
    telefone = TextField() 
    celular = TextField()
    obs = TextField()
    cod_cli = TextField()
    ie = TextField()
    nome = TextField()
    endereco = TextField()
    cidade = TextField()
    estado = TextField()
    cep = TextField()
   
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
    gravacao2 = TextField()
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
    id_Linha = IntegerField()
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
    id_cliente = IntegerField()
    ano = IntegerField()
    cod_func = IntegerField()
    cod_item = IntegerField()
    data = DateTimeField(default=datetime.datetime.now)
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
    cnpj = TextField()
    email = TextField() 
    qntcompras = IntegerField()
    cod_for = TextField()
    nome = TextField()
    ie = TextField()
    endereco = TextField()
    cidade = TextField()
    estado = TextField()
    cep = TextField()
    telefone = TextField()
    fax = TextField()
    
    obs = TextField()
   
    class Meta:
        db_table = 'Fornecedores'
        database = db
    
class Ferramenta(Model):
    ID = PrimaryKeyField()
    Ferramenta = TextField()
    Cod_ferramenta = TextField()
    cod_cli = IntegerField()
    mm = IntegerField()
    class Meta:
        db_table = 'ferramenta'
        database = db

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
        db_table = 'pedidos'
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
    inicio = TextField(default = str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute))
    fim =  TextField(default = str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute))
    desc = TextField()
    class Meta:
        db_table = 'ponto'
        database = db

class Material(Model):
    ID = PrimaryKeyField()
    nome = TextField()
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

class itens(Model):
    id= PrimaryKeyField()
    descricao= TextField()
    codigo=TextField()
    material= TextField()
    esp1= TextField()
    esp2= TextField()
    esp3= TextField()
    class Meta:
        db_table = 'itens'
        database = db

class linha(Model):
    id= PrimaryKeyField()
    nome= TextField()
    numero_inicial = IntegerField()
    class Meta:
        db_table = 'linha'
        database = db

class item(Model):
    id = PrimaryKeyField()
    descricao = TextField()
    codigo = TextField()
    cod_mat = TextField()
    esp1 = TextField()
    esp2 = TextField()
    esp3 = TextField()
    class Meta:
        db_table = 'itens'
        database = db