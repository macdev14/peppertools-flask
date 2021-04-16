# -*- coding: utf-8 -*-
from helper import *
from flask_qrcode import QRcode 
from flask import Flask, send_from_directory, redirect,render_template, request, session, flash, jsonify, make_response
from flask_cors import  CORS, cross_origin
from flask_session.__init__ import Session
from flask_session import Session
from tempfile import mkdtemp
from flask_socketio import SocketIO
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import sys, os, jwt, json
from jinja2 import Undefined
import datetime
from datetime import date
import pytz
import re
import requests
from playhouse.shortcuts import model_to_dict, dict_to_model
from model import *
from page import *

"""os.environ['SECRET_KEY'] =  "caf3cc4546725599c99158599d443fc815bd137b73b0b69bc804f3ba483aeaa224c75a2b3fc1f35eccfdfef6cdd01858450435ef6daed0c49bf01fbe1e7b3b79"
os.environ['DB'] =  "mysql://rkpmtiv6bbvm81e5:bfm5w4ohfjp7ldw8@nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ztqqdjf98kpnzn4nn "
os.environ['HOST']= "nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
os.environ['USER'] =  "rkpmtiv6bbvm81e5"
os.environ['PASSWORD'] = "yz1mq64u3h1sab93"
os.environ['DATABASE'] = "ztqqdjf98kpnzn4n"


db = SQL(os.environ['DB'])"""

#db = SQL("sqlite:///peppertools.db")

app = Flask(__name__)
app.add_template_global(get_level,name='get_level')
JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined, '' : None,  'get_level': get_level}



socketio = SocketIO(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'caf3cc4546725599c99158599d443fc815bd137b73b0b69bc804f3ba483aeaa224c75a2b3fc1f35eccfdfef6cdd01858450435ef6daed0c49bf01fbe1e7b3b79'
#SESSION_COOKIE_DOMAIN = 'peppertools.herokuapp.com'
os.environ['SECRET_KEY'] = 'caf3cc4546725599c99158599d443fc815bd137b73b0b69bc804f3ba483aeaa224c75a2b3fc1f35eccfdfef6cdd01858450435ef6daed0c49bf01fbe1e7b3b79'
app.config["SECRET_KEY"] = 'caf3cc4546725599c99158599d443fc815bd137b73b0b69bc804f3ba483aeaa224c75a2b3fc1f35eccfdfef6cdd01858450435ef6daed0c49bf01fbe1e7b3b79'
QRcode(app)
TEMPLATE_FOLDER = '/templates/'
HTML_FILE = 'layout.html'
#app.add_template_global(name=HTML_FILE, f=TEMPLATE_FOLDER)




@app.before_request
def before_request():
    """Connect to the database before each request"""
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers['Access-Control-Allow-Origin'] = '*'
   # response.headers["authorization"] = session.get('_permanent')
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, Authorization, Origin, X-Requested-With, Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    return response

#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/')
@login_required
@managerLevel

def index():
    os = os_em_historico()
    #os = Cadastro_OS.select(Cadastro_OS.Id, Cadastro_OS.Numero_Os).join(Historico_os, on=(Cadastro_OS.Id == Historico_os.id_os)).distinct()
    #historico_os = Historico_os.select().dicts()
   
    response = Response(render_template("home.html", title= "Inicio", auth=session.get('token'), historico_os=os,active1="active",active2="", active3="", active4=""))
   # #print(session.get('token'))
    response.headers['authorization'] = session.get('_permanent')
    return response

@app.route('/historico')
@login_required
@managerLevel
def historico():
    os = Cadastro_OS.select(Cadastro_OS.Id, Cadastro_OS.Numero_Os).join(Historico_os, on=(Cadastro_OS.Id == Historico_os.id_os)).distinct()
"""@app.route('/estoque')
@login_required
def estoque():
    keys = Estoque._meta.fields.keys()
    columns = list(keys)
    columns.remove('id_cliente')
    columns.remove('ID')
    columns.remove('data')
    response = Response(render_template("list.html", title= "Estoque", client = True, tableCol=columns, table="estoque", columns=columns, col_len=len(columns), active1="",active2="active", active3="", active4=""))
   # #print(session.get('token'))
    response.headers['authorization'] = session.get('_permanent')
    return response"""


@app.route('/clientes')
@login_required
@managerLevel
def clientes():
    #return getClientes("key","*")
    return render_template("clientes.html", auth=session.get('token'), title="Clientes", active1="",active2="", active3="", active4="active")


@app.route('/clientes/buscar')
@login_required
@managerLevel
def search():
    return underdev()


@app.route('/clientes/form/', methods=["GET", "POST"])
@login_required
@managerLevel
def cadCli():
    if request.method == 'GET':
        clientes = list(Clientes._meta.fields.keys())
        return render_template("Form.html", TableCol=clientes, TableLen = len(clientes), table='clientes' , edit=False, id=id, active1="",active2="", active3="", active4="active")
       # return render_template("client_edit.html", clientes2=clientes, cliLen=len(clientes), edit=False, id=id, active1="",active2="", active3="active", active4="")
    elif request.method == 'POST':   # clientes = getData(" ","*", "Clientes")
        try:
            if request.form:
                data = dict(request.form)
                
                Clientes.create(cod_cli=request.form['cod_cli'], nome = request.form['nome'], cnpj=request.form['cnpj'], ie = request.form['ie'], endereco=request.form['endereco'], cidade=request.form['cidade'], cep=request.form['cep'], telefone=request.form['telefone'], celular=request.form['celular'], obs=request.form['obs'])
                idCli = Clientes.select(fn.MAX(Clientes.ID)).scalar()
                flash('Cliente cadastrado com sucesso')
                ##print(request.form)
                return redirect('/clientes/form/'+ str(idCli))
            else:
                raise Exception("Empty")
        except:
            return redirect('/clientes/form/')

@app.route('/clientes/form/<int:cliId>', methods = ['POST', 'GET'])
@login_required
@managerLevel
def editCli(cliId):
    if request.method == 'GET':
        clientes = Clientes.select().where(Clientes.ID == cliId)
        if not clientes:
            flash('Erro ao encontrar cliente.')
            return redirect('/clientes/form/')
        clientesCol = list(Clientes._meta.fields.keys())
        cliLen = len(clientesCol)
       # #print(clientes)
        return render_template("Form.html", table='clientes', content=clientes[0], TableLen=cliLen, TableCol=clientesCol, id=cliId, edit=True, active1="",active2="", active3="active", active4="") 
    elif request.method == 'POST':
        if request.form:
            #Clientes.update()
            Clientes.update(cod_cli=request.form['cod_cli'], nome = request.form['nome'], cnpj=request.form['cnpj'], ie = request.form['ie'], endereco=request.form['endereco'], cidade=request.form['cidade'], cep=request.form['cep'], telefone=request.form['telefone'], celular=request.form['celular'], obs=request.form['obs']).where(Clientes.ID == cliId).execute()
            #updateData(dict(request.form), 'Clientes', 'ID', cliId)
            flash('Cliente alterado com sucesso')
        return redirect('/clientes/form/'+ str(cliId))
        
@app.route("/os")
@login_required
@managerLevel
def osAll():
    try:
        session.pop('osid')
    except:
        pass
        
    return render_template("os.html", auth=session.get('token'), active1="",active2="", active3="", active4="active", title="Ordem de Serviço")     


@app.route("/os/imprimir")
@login_required
@managerLevel
def print1():
    #return render_template("imprimir_os.html", title= "Inicio", active1="active",active2="", active3="", active4="active")
    return underdev()


@app.route("/os/buscar")
@login_required
@adminLevel
def buscar():
    #return render_template("buscar_os.html", title= "Inicio", active1="",active2="", active3="", active4="active")
    return underdev()


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    if not request.is_secure and app.env != "development":
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code) """
    tz = pytz.timezone('America/Sao_Paulo')
    x = datetime.datetime.now(tz=tz)
    date = x.strftime("%d/%m/%Y")
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        return login_user(user, password, os.environ['SECRET_KEY'])
    else:    
        return render_template('login.html', date = date)


@app.route('/logout')
@login_required
def logout():
    return logoutCommit()


@app.route("/os/total")
@login_required
def all():
    nos = Cadastro_OS.select(fn.MAX(Cadastro_OS.Id)).get()
    return jsonify(nos)


@app.route('/os/form/', methods=["POST", "GET"])
@login_required
@managerLevel
def new_os():
    #clients = db.execute('SELECT DISTINCT Clientes.ID, nome FROM Cadastro_OS, Clientes WHERE Cadastro_OS.id_cliente = Clientes.ID')
        clients = Clientes.select(Clientes.ID, Clientes.nome).join(Cadastro_OS, on=(Cadastro_OS.Id_Cliente == Clientes.ID)).distinct()

        x = datetime.datetime.now()
        date = x.strftime("%d/%m/%Y")
        #os_num = db.execute('SELECT MAX(Numero_Os) AS num_os FROM Cadastro_OS')
        os_num = int(Cadastro_OS.select(fn.MAX(Cadastro_OS.Numero_Os)).scalar())+1
        clients_len = len(clients)
        if request.method == 'POST':
            try:
                if request.form['Id_Cliente'] == 0 or request.form['Id_Cliente'] == '0':
                    flash('Selecione um cliente')
                    return redirect('/os/form/')
                data = dict(request.form)
            # data = json.loads(data)
                Cadastro_OS.create(Tipo=request.form['Tipo'], Numero_Os = request.form['Numero_Os'],
                    Ferramenta = request.form['Ferramenta'], Desenho_Cliente= request.form['Desenho_Cliente'],
                    Desenho_Pimentel= request.form['Desenho_Pimentel'], gravacao2 = request.form['gravacao2'],
                    Id_Cliente = request.form['Id_Cliente'], Data = request.form['Data'], unidade = request.form['unidade'],
                    Prazo = request.form['Prazo'], Data_Pedido = request.form['Data_Pedido'], 
                    Data_Nf = request.form['Data_Nf'], Especificacao = request.form['Especificacao'], Quantidade = request.form['Quantidade'],
                    Numero_Nf = request.form['Numero_Nf'], Numero_Pedido = request.form['Numero_Pedido'], STATUS = int(request.form['STATUS'], id_Linha=request.form['id_Linha']),
                    )
                

                idos = Cadastro_OS.select(fn.MAX(Cadastro_OS.Id)).scalar()
                idproc = request.form['STATUS']
                registerprocess(idproc, idos, request.form['Data'], '')
                
                flash('O.S cadastrada com sucesso')
              
                return redirect('/os/form/'+ str(idos))
            except:
                flash("Erro ao cadastrar")
                return redirect('/os/form/')
        
        processes = processos.select()
        linha_os = linha.select(linha.id, linha.nome)
        return render_template('os_gen.html', clients = clients, clients_len = clients_len, os_num = os_num, field = '' , data = date, processes= processes, linha= linha_os, title="Ordem de Serviço")


@app.route('/os/form/<int:osid>', methods = ['POST', 'GET'])
@login_required
@managerLevel
def os_edit(osid):
    if request.method == 'POST':
        if not 'id_Linha' in request.form:
            flash('Selecione uma Linha de Produto')
            return redirect('/os/form/'+str(osid))
        elif not 'Id_Cliente' in request.form:
            flash('Selecione um Cliente')
            return redirect('/os/form/'+str(osid))
        data = dict(request.form)
        try:
            data['Numero_Os'] = int(data['Numero_Os'])
            data['Id_Cliente'] = int(data['Id_Cliente'])
            data['Numero_Nf'] = int(data['Numero_Nf'])
            data['Numero_Pedido'] = int(data['Numero_Pedido'])
            data['Quantidade'] = int(data['Quantidade'])
            data['Id'] = int(data['Id'])
            data['STATUS'] = int(data['STATUS'])
            data['Data'] = datetime.datetime.strptime(str(data['Data']), '%d/%m/%Y').strftime('%Y-%m-%d')
            data['Data_Pedido'] = datetime.datetime.strptime(str(data['Data_Pedido']), '%m/%d/%Y').strftime('%Y-%m-%d')
            data['Prazo'] = datetime.datetime.strptime(str(data['Prazo']), '%d/%m/%Y').strftime('%Y-%m-%d')
            data['Data_Nf'] = datetime.datetime.strptime(str(data['Data_Nf']), '%d/%m/%Y').strftime('%Y-%m-%d')
        except:
            pass
        os = Cadastro_OS.select().where(Cadastro_OS.Id == osid).get()
        if not os.STATUS or int(data['STATUS']) != int(os.STATUS):
            try:
                registerprocess(int(data['STATUS']), os.Id, request.form['Data'], '')
            except:
                pass
       
        os.Numero_Os = data['Numero_Os']
        os.Id_Cliente =  data['Id_Cliente']
        os.Numero_Nf = data['Numero_Nf']
        os.Tipo = data['Tipo']
        os.Especificacao = re.sub(r'\s', '', data['Especificacao'])
        os.Numero_Pedido = data['Numero_Pedido']
        os.Quantidade = data['Quantidade']
        os.Material = data['Material']
        os.Data = data['Data']
        os.Data_Pedido = data['Data_Pedido']
        os.Prazo = data['Prazo']
        os.unidade = data['unidade']
        os.Data_Nf = data['Data_Nf']
        os.gravacao = re.sub(r'\s', '',data['gravacao'])
        os.Desenho_Cliente = re.sub(r'\s', '',data['Desenho_Cliente'])
        os.Desenho_Pimentel = re.sub(r'\s', '', data['Desenho_Pimentel'])
        os.STATUS = int(data['STATUS'])
        os.id_Linha = int(data['id_Linha'])
        os.save()
        

        flash('O.S alterada com sucesso')
        
        if session.get('osid'):
           session.pop('osid')
        return redirect('/os/form/'+ str(osid))
    else:
       
        if session.get('osid') is not None:
            osid = session.get('osid')
        clients = Clientes.select(Clientes.ID, Clientes.nome).join(Cadastro_OS, on=(Cadastro_OS.Id_Cliente == Clientes.ID)).distinct()
        os_num = int(Cadastro_OS.select(fn.MAX(Cadastro_OS.Numero_Os)).scalar())+1
        os = Cadastro_OS.select().where(Cadastro_OS.Id == osid)
        os = [model_to_dict(o) for o in os]
        if not os:
            return redirect('/os/form/')
        
        field = os[0]
        if field['Data_Pedido']:
            field['Data_Pedido'] =datetime.datetime.strptime( str(field['Data_Pedido']), '%Y-%m-%d').strftime('%d/%m/%Y')
        if not field['Data']:
            field['Data'] = datetime.datetime.now().strftime('%d/%m/%Y')
        else:
            field['Data'] = datetime.datetime.strptime( str(field['Data']), '%Y-%m-%d').strftime('%d/%m/%Y')
        if field['Prazo']:
            field['Prazo'] = datetime.datetime.strptime( str(field['Prazo']), '%Y-%m-%d').strftime('%d/%m/%Y')
        if field['Data_Nf']:
            field['Data_Nf'] = datetime.datetime.strptime( str(field['Data_Nf']), '%Y-%m-%d').strftime('%d/%m/%Y')
        
        x = datetime.datetime.now()
        date = x.strftime("%d/%m/%Y")
        idproc = Cadastro_OS.select(Cadastro_OS.STATUS).where(Cadastro_OS.Id == int(osid)).dicts()
        idproc = idproc[0]["STATUS"]
        if idproc and int(idproc):
            procinfo = processos.select().where(processos.ID == idproc).dicts()
            procinfo = procinfo[0]
        else:
            procinfo = None
        processes = processos.select()
        linha_os = linha.select(linha.id, linha.nome)
        return render_template('os_gen.html', clients = clients, clients_len = len(clients), os_num = int(os_num), field = field , data = date, processes=processes, procinfo=procinfo, linha=linha_os, title="Ordem de Serviço")
        

@app.route('/os/form/delete/<int:osid>', methods = ['POST', 'GET'])
@login_required
@managerLevel
def os_del(osid):
    if request.method == 'GET':
        try:
            Cadastro_OS.delete().where(Cadastro_OS.Id == osid).execute()
            flash('O.S deletada com sucesso')
            return redirect('/os/form/')
        except:
            flash('Erro ao deletar O.S')
            return redirect('/os/form/'+str(osid))
    flash('Erro ao deletar O.S')
    return redirect('/os/form/')


@app.route("/register", methods=["GET", "POST"])
@adminLevel
def register():
    if request.method == 'POST':
       
        rows = usuarios.select().where(usuarios.ds_login == request.form.get("username"))
        rows=[model_to_dict(row) for row in rows]
            #rows = db.execute("SELECT * FROM usuarios WHERE ds_login = \'"+ request.form.get("username") + "\'")
        rowsPass = usuarios.select().where(usuarios.ds_login == request.form.get("username"))
        rowsPass=[model_to_dict(row) for row in rowsPass]
            #rowsPass = db.execute("SELECT * FROM usuarios WHERE ds_senha = "+ generate_password_hash(request.form.get("password")))
        if len(rows) == 1 or len(rowsPass) == 1:
            flash("User or password already exists")
            return redirect("/register")
        if request.form.get("password") != request.form.get("password-confirm"):
            flash("Senhas não coincidem")
            return redirect("/register")

        if request.form.get("key") != "12@Afiado#45":
            flash("Chave inválida")
            return redirect("/register")
            # Ensure username was submitted
       
       
        usuarios.create(ds_login=request.form.get('username'), ds_senha=generate_password_hash(request.form.get('password')), nivel=request.form.get('nivel'))
                #stmt = "INSERT INTO usuarios(ds_login, ds_senha, nivel) VALUES(\'" + request.form.get('username') + "\', \'" + generate_password_hash(request.form.get('password')) + "\', " + request.form.get('nivel') + ")"
                ##print(stmt)
                #db.execute(stmt)
        flash("Usuário cadastrado com sucesso. Faça seu login.")
        return logoutCommit()
                
                

            # Query database for username
                
        
        # Ensure username exists and password is correct
    return render_template("register.html")
  

@app.route('/os/form/print/<int:osid>', methods = ['GET'])
@login_required
def print_os(osid):
    #print(osid)
    if request.method == 'GET':
        laprocessos =  list(Cadastro_OS.select(Cadastro_OS.Numero_Os, Cadastro_OS.Tipo, Historico_os.qtd ,processos.Nome, Historico_os.periodo, Historico_os.inicio, Historico_os.fim, Historico_os.data, Historico_os.ID, Clientes.nome).from_(Cadastro_OS, processos, Historico_os, Clientes).distinct().where(Historico_os.id_os == Cadastro_OS.Id, Historico_os.id_proc == processos.ID, Cadastro_OS.Id==osid, Cadastro_OS.Id_Cliente == Clientes.ID).order_by(Cadastro_OS.Numero_Os.desc(), Historico_os.ID.desc(), Historico_os.periodo.desc()).dicts())
        #laprocessos = os_em_andamento(py=True)
        print(laprocessos)
        #laprocessos = laprocessos[0]
        #print("1--1---1")
        #print(laprocessos)
        rows = list(Cadastro_OS.select().where(Cadastro_OS.Id == osid).dicts())
        maxPeriod = Historico_os.select(fn.MAX(Historico_os.periodo)).where(Historico_os.id_proc == rows[0]['STATUS']).scalar()
        #print(rows[0])
        allProcessos = list(processos.select(Historico_os.id_proc, processos.Nome, processos.ID).from_(processos, Historico_os).where(processos.ID == Historico_os.id_proc, Historico_os.id_os == osid, Historico_os.periodo==maxPeriod).dicts())
        #print(allProcessos)
        #os = getOs(osid)
        if not os:
            flash("O.S não encontrada.")
            return redirect("/")
        field = rows[0]
        res = list(Clientes.select(Clientes.nome, Clientes.ID).from_(Clientes, Cadastro_OS).where(Cadastro_OS.Id_Cliente == Clientes.ID, Cadastro_OS.Id == osid).dicts())
        ##print(res)
        tok = jwt.encode({'osid': str(osid)}, os.environ['SECRET_KEY']).decode('UTF-8')
        qr = "https://peppertools.herokuapp.com/os/"+str(tok)
        field['nome'] = res[0]['nome']
        field['Data_digit'] = datetime.datetime.strptime(str(field['Data']), '%Y-%m-%d').strftime('%y')
        field['Data'] = checkDate(field['Data'])
        field['Data_Nf'] = checkDate(field['Data_Nf'])
        field['Data_Pedido'] = checkDate(field['Data_Nf'])
        field['Prazo'] = checkDate(field['Prazo'])
        try:
            session.pop('osid')
        except:
            pass    
        return render_template("imprimir_os.html", field = field, qr=qr, processes=laprocessos)
      

@app.route('/os/<string:osid>', methods = ['POST', 'GET'])
def access(osid):
   
    uncrypt = jwt.decode(osid, os.environ['SECRET_KEY'], algorithms=['HS256'])
    session['osid'] = uncrypt['osid']
    return redirect('/login')
    
   



@app.route('/estoque/form/', methods = ['POST', 'GET'])
@login_required
def cadEstoque():
    clients = Clientes.select(Clientes.nome, Clientes.ID)
        #clientes = list(Estoque._meta.fields.keys())
    estKeys = list(Estoque._meta.fields.keys())
        #clientes = clientes[0]
    if request.method == 'POST' and request.form: 
        #3 try:      
        data = dict(request.form)
        if not data['data']:
            data['data'] = datetime.datetime.now().strftime('%d/%m/%Y')
        else:    
            try:
                data['data'] =  datetime.datetime.strptime(data['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
                flash('Item cadastrado com sucesso')
            except:
                data['data'] = datetime.datetime.now().strftime('%Y-%m-%d')
                flash('Erro ao cadastrar data')
                pass
        Estoque.create(id_cliente=data['id_cliente'], ferramenta=data['ferramenta'], material=data['material'], cod_pc=data['cod_pc'], mm=data['mm'], qt=data['qt'], gaveta=data['gaveta'], data=data['data'])
        idEst = Estoque.select().order_by(Estoque.ID.desc()).get()
            #idCli = insertData(data, 'Estoque')
        
        #print(request.form)
        return redirect('/estoque/form/'+ str(idEst))
    data = datetime.datetime.now().strftime('%d/%m/%Y')
    select2 = list(itens.select().dicts())
    pagefunc = page('Estoque', select=clients, select2=select2, edit=False)
    return pagefunc.render()
    #return render_template("Form.html", TableCol=estKeys, data=data, clients = clients, TableLen = len(estKeys), cliLen = len(clients), cliCol = 'id_cliente', table='estoque' , edit=False, id=id, active1="",active2="", active3="active", active4="")
         #except:
                #flash("Erro ao cadastrar item!")
                #return redirect('/estoque/form/')

@app.route('/estoque/form/<int:estId>', methods = ['POST', 'GET'])
@login_required
def editEstoque(estId):
    clients = Clientes.select(Clientes.nome, Clientes.ID)

    #clients = db.execute('SELECT DISTINCT Clientes.ID, nome FROM Cadastro_OS, Clientes WHERE Cadastro_OS.Id_Cliente = Clientes.ID')
    if request.method == 'GET':
        try:
            estoque = Estoque.select(Estoque, Clientes.ID, Clientes.nome).from_(Estoque, Clientes).where(Estoque.id_cliente == Clientes.ID, Estoque.ID == estId) #getData(" ", "*", "Estoque WHERE ID = "+ str(estId))
            estoque = [model_to_dict(item) for item in estoque]
            #print(estoque)
            try:
                estoque[0]['data'] = estoque[0]['data'].strftime("%d/%m/%Y")
            except:
                pass
            estoqueCol = list(Estoque._meta.fields.keys())
            estLen = len(estoqueCol)
        # #print(clientes)
            pagefunc = page('Estoque', select=clients, select2=select2, edit=True)
            return pagefunc.render()
            #return render_template("Form.html", table='estoque', content=estoque[0], cliLen = len(clients), clients = clients, cliCol = 'id_cliente',TableCol=estoqueCol, TableLen = estLen, id=estId, edit=True, active1="",active2="", active3="active", active4="") 
       
        except:
            return redirect('/estoque/form/')
        
        
        
           
    elif request.method == 'POST' and request.form:
            ##print(request.form)
        data = dict(request.form)
        if not data['data']:
            data['data'] = datetime.datetime.now().strftime('%d/%m/%Y')
        else:    
            try:
                data['data'] =  datetime.datetime.strptime(data['data'], '%d/%m/%Y').strftime('%d/%m/%Y')
            except:
                flash('Erro ao alterar Item.')
                return redirect('/estoque/form/'+ str(estId))
        
        #data['data'] = checkDate(data['data'])
        data['id_cliente'] = int(data['id_cliente'])
        data['qt'] = int(data['qt']) 
        data['gaveta'] = int(data['gaveta'])
        #data['data'] = datetime.datetime.strptime(data['data'], "%Y-%m-%d").strftime('%Y-%m-%d')
        item = Estoque.select().where(Estoque.ID == estId).get()
        item.gaveta = data['gaveta']
        item.qt = data['qt']
        item.mm = data['mm']
        item.ferramenta = data['ferramenta']
        item.id_cliente = data['id_cliente']
        item.data = data['data']
        item.save()
        flash('Item alterado.')
        return redirect('/estoque/form/'+ str(estId))


@app.route('/orcamento/form/', methods=['POST', 'GET'])
@login_required
def invoice():
    Keys = list(orcamento._meta.fields.keys())
    data = datetime.datetime.now().strftime('%d/%m/%Y')
    if request.method == 'POST' and request.form:
        #try:
        orcamento.create(numero=request.form['numero'], ano = request.form['ano'], cod_item=request.form['cod_item'], data= request.form['data'], cod_func=request.form['cod_func'], id_cliente=request.form['id_cliente'],prazo_entrega=request.form['prazo_entrega'], prazo_pagto=request.form['prazo_pagto'], ipi=request.form['ipi'], icms=request.form['icms'])
        idorcam = orcamento.select(fn.MAX(orcamento.ID)).scalar()
        flash('Cadastrado com sucesso!')
        return redirect('/orcamento/form/'+ str(idorcam))
        #except:
        #    flash('Erro ao cadastrar!')
    funcionario = funcionarios.select(funcionarios.id, funcionarios.nome)
    items = Estoque.select(Estoque.ferramenta, Estoque.ID)
    clients = Clientes.select(Clientes.nome, Clientes.ID)
    num = orcamento.select(fn.MAX(orcamento.numero)).scalar()
    pager = page(table='orcamento', edit=False, select = clients , select2=funcionario , select3=items)
    return pager.render()
        #return render_template("Form.html", TableCol=Keys, clients=items, cliLen= len(items), selection2=clients, sel2Col='id_cliente', sel2Len=len(clients), cliCol = 'cod_item' ,data=data, TableLen = len(Keys), table='orcamento' , edit=False, numfield=num ,active1="",active2="", active3="active", active4="")
 

@app.route('/orcamento/form/<int:inid>', methods=['POST', 'GET'])
@login_required
def invoiceEdit(inid):
    if request.method == 'POST':
        if request.form['cod_item'] and request.form['id_cliente'] and request.form['cod_func']:
            orcamento.update(numero=request.form['numero'], ano=request.form['ano'], cod_item=request.form['cod_item'], data=request.form['data'], id_cliente = request.form['id_cliente'], cod_func=request.form['cod_func'], prazo_entrega=request.form['prazo_entrega'], prazo_pagto=request.form['prazo_pagto'], ipi=request.form['ipi'], icms=request.form['icms']).where(orcamento.ID == inid).execute()
        flash('Verifique os campos.')
        return redirect('/orcamento/form/'+ str(inid))
    funcionario = funcionarios.select(funcionarios.id, funcionarios.nome)
    Keys = list(orcamento._meta.fields.keys())
    clients = list(Clientes.select(Clientes.nome, Clientes.ID).dicts())
    items = list(Estoque.select(Estoque.ferramenta, Estoque.ID).dicts())
    invoice = orcamento.select().where(orcamento.ID == inid)
    pager = page(table = 'orcamento', content = invoice[0], edit=True, select = clients , select2=funcionario, select3=items)
    return pager.render()
    
    
    
    #return render_template("Form.html", content=invoice[0], clients=items, cliLen= len(items), cliCol = 'cod_item', selection2=clients, sel2Col='id_cliente', sel2Len=len(clients), TableCol=Keys, TableLen = len(Keys), table='orçamento' , edit=True, id=inid, active1="",active2="", active3="active", active4="")

@app.route('/list')
def listing():
    return render_template('table.html')

@app.route('/contasapagar/form/', methods=['POST', 'GET'])
@login_required
@financialLevel
def contaspagar():
    forn = Fornecedores.select(Fornecedores.nome, Fornecedores.ID)
    Keys = list(contasapagar._meta.fields.keys())
    if request.method == 'POST':
       # try:
        contasapagar.create(vencimento=datetime.datetime.strptime(request.form['vencimento'], '%d/%m/%Y').strftime('%d/%m/%Y'), descricao= request.form['descricao'], valor=float(request.form['valor'].strip()), pago=float(request.form['pago'].strip()), data_pagamento=datetime.datetime.strptime(request.form['data_pagamento'], "%d/%m/%Y").strftime("%d/%m/%Y"), cod_fornecedor=int(request.form['cod_fornecedor']))
        idconta = contasapagar.select(fn.MAX(contasapagar.ID)).scalar()
        flash('Cadastrado com Sucesso')
        return redirect('/contasapagar/form/'+ str(idconta))
     #   except: 
        #flash('Erro ao Cadastrar')
       # return redirect('/contasapagar/form/')
    return render_template("Form.html", TableCol=Keys, TableLen = len(Keys), clients=forn, cliCol = 'id_cliente', cliLen= len(forn), table='contasapagar' , edit=False, active1="",active2="", active3="active", active4="")

@app.route('/contasapagar/form/<int:idconta>', methods = ['POST', 'GET'])
@login_required
@financialLevel
def editarcontas(idconta):
    forn = Fornecedores.select(Fornecedores.nome, Fornecedores.ID)
    Keys = list(contasapagar._meta.fields.keys())
    conta = list(contasapagar.select().where(contasapagar.ID == idconta).dicts())
    try:
        conta[0]['vencimento'] = datetime.datetime.strptime(conta[0]['vencimento'] , '%Y-%m-%d').strftime('%d/%m/%Y')
        conta[0]['data_pagamento'] = datetime.datetime.strptime(conta[0]['vencimento'] , '%Y-%m-%d').strftime('%d/%m/%Y')
    except:
        pass
    if request.method == 'POST':
        try:  
            contasapagar.update(vencimento=datetime.datetime.strptime(request.form['vencimento'], "%d/%m/%Y").strftime("%Y-%m-%d"), descricao= request.form['descricao'], valor=float(request.form['valor'].strip()), pago=float(request.form['pago'].strip()), data_pagamento=datetime.datetime.strptime(request.form['data_pagamento'], "%d/%m/%Y").strftime("%d/%m/%Y"), cod_fornecedor=int(request.form['cod_fornecedor'])).execute()
            flash('Alterado com Sucesso')
            return redirect('/contasapagar/form/'+ str(idconta))
        except:
            flash('Erro ao alterar')
            return redirect('/contasapagar/form/'+ str(idconta))
    return render_template("Form.html", content=conta[0], TableCol=Keys, TableLen = len(Keys), clients=forn, cliCol = 'cod_fornecedor',cliLen= len(forn),table='contasapagar' , edit=True, id=idconta, active1="",active2="", active3="active", active4="")

@app.route("/fornecedores/form/", defaults={"idfor": ''}, methods = ['POST', 'GET'])
@app.route('/fornecedores/form/<int:idfor>', methods = ['POST', 'GET'])
@login_required
@financialLevel
def fornecedor(idfor):
    Keys = list(Fornecedores._meta.fields.keys())
    if idfor != '':
        if request.method == 'POST':
            try:
                Fornecedores.update(cod_for=request.form['cod_for'], nome= request.form['nome'], cnpj=request.form['cnpj'], ie= request.form['ie'], endereco= request.form['endereco'], cidade=request.form['cidade'], estado=request.form['estado'], cep=request.form['cep'], telefone=request.form['telefone'], celular=request.form['celular'], email=request.form['email'], obs=request.form['obs'], qntcompras=request.form['qntcompras']).where(Fornecedores.ID == idfor).execute()
                flash('Alterado com sucesso')
            except:
                flash('Erro ao alterar Fornecedor')
            return redirect('/fornecedor/form/'+str(idfor))
        fornecedor = Fornecedores.select().where(Fornecedores.ID == idfor)
        return render_template("Form.html", content=fornecedor[0], TableCol=Keys, TableLen = len(Keys), table='fornecedor' , edit=True, id=idfor, active1="",active2="", active3="active", active4="")
    if request.method == 'POST':
        try:
            data = dict(request.form)
            if not isinstance(data['qntcompras'], int):
                data['qntcompras'] = 0
                flash('Erro ao cadastrar campo(s)')
            Fornecedores.create(cod_for=request.form['cod_for'], nome= request.form['nome'], cnpj=request.form['cnpj'], ie= request.form['ie'], endereco= request.form['endereco'], cidade=request.form['cidade'], estado=request.form['estado'], cep=request.form['cep'], telefone=request.form['telefone'], celular=request.form['celular'], email=request.form['email'], obs=request.form['obs'], qntcompras=int(data['qntcompras']))
            idforn = Fornecedores.select(fn.MAX(Fornecedores.ID)).scalar()
            flash('Cadastrado com sucesso')
            return redirect('/fornecedor/form/'+str(idforn))
        except:
            flash('Erro ao cadastrar campo(s)')
    return render_template("Form.html", TableCol=Keys, TableLen = len(Keys), table='fornecedor' , edit=False, active1="",active2="", active3="active", active4="")


@app.route('/compras/form/', defaults={'idcompra': ''}, methods=['POST', 'GET'])
@app.route('/compras/form/<int:idcompra>', methods=['POST', 'GET'])
@login_required
@financialLevel
def comprasform(idcompra):
    Keys = list(compras._meta.fields.keys())
    fornecedores = Fornecedores.select(Fornecedores.ID, Fornecedores.nome)
    fornecedores_len = len(fornecedores)
    if idcompra != '':
        if request.method == 'POST':
            data = dict(request.form)
            try:
                try:
                    data['qnt'] = int(data['qnt'])
                except:
                    data['qnt']=0  
                    flash('Erro ao alterar Quantidade')
                try:
                    data['preco'] = float(data['preco'])
                except: 
                    data['preco'] = 0.00
                    flash('Erro ao alterar preco')

                data['data'] = datetime.datetime.strptime(data['data'], '%d/%m/%Y').strftime('%d/%m/%Y')    
                data['prazo'] =  datetime.datetime.strptime(data['prazo'], '%d/%m/%Y').strftime('%d/%m/%Y') 

                
                compras.update(cod_fornecedor=request.form['cod_fornecedor'], data=data['data'], qnt=int(data['qnt']), preco= float(data['preco']), desc= request.form['desc'], ipi=request.form['ipi'], prazo=data['prazo'], cond=request.form['cond'], contato=request.form['contato']).where(compras.ID == idcompra).execute()
                compra = compras.select(compras, Fornecedores.ID, Fornecedores.nome).from_(compras, Fornecedores).where(compras.cod_fornecedor == Fornecedores.ID, compras.ID == idcompra)    
                flash('Alterado com sucesso')
        
            except:
                flash('Erro ao alterar Compra')
            return redirect('/compras/form/'+str(idcompra))
        compra = compras.select().where(compras.ID == idcompra)
        if not compra:
            return redirect('/compras/form/')
        return render_template("Form.html", content=compra[0], clients=fornecedores, cliLen= fornecedores_len, cliCol='cod_fornecedor',TableCol=Keys, TableLen = len(Keys), table='compras' , edit=True, id=idcompra, active1="",active2="", active3="active", active4="")
    if request.method == 'POST':
      #  try:
            data = dict(request.form)
            try:
                data['qnt'] = int(data['qnt'])
            except:
                data['qnt']=0
                flash('Erro ao cadastrar Quantidade')
            try:
                data['preco'] = float(data['preco'])
            except:
                data['preco'] = 0.00
                flash('Erro ao cadastrar preco')

            compras.create(cod_fornecedor=request.form['cod_fornecedor'], data=data['data'], qnt=int(data['qnt']), preco= float(data['preco']), desc= request.form['desc'], ipi=request.form['ipi'], prazo=data['prazo'], cond=request.form['cond'], contato=request.form['contato'])
            
            idcompra = compras.select(fn.MAX(compras.ID)).scalar()
            flash('Cadastrado com sucesso')
            return redirect('/compras/form/'+str(idcompra))
     #   except:
     #       flash('Erro ao cadastrar campo(s)')
    return render_template("Form.html", TableCol=Keys, TableLen = len(Keys), table='compras', clients=fornecedores , cliLen= fornecedores_len, edit=False, active1="",active2="", active3="active", active4="")


@app.route('/notafiscal/form/', defaults={'idnota': ''}, methods=['POST', 'GET'])
@app.route('/notafiscal/form/<int:idnota>', methods=['POST', 'GET'])
@login_required
@financialLevel
def nfform(idnota):
    Keys = list(notafiscal._meta.fields.keys())
    if idnota != '':
        if request.method == 'POST':
            data = dict(request.form)
            try:
                try:
                    data['numero_nf'] = int(data['numero_nf'])
                except:
                    data['numero_nf']=0  
                    flash('Erro ao alterar Numero NF')
                try:    
                    data['valor_nf'] = float(data['valor'])
                except:
                    data['valor_nf'] = 0.00
                    flash('Erro ao alterar valor')

                notafiscal.update(
                    numero_nf=request.form['numero_nf'], 
                    data_nf=data['data_nf'], valor_nf=data['valor_nf'],  
                    desc= request.form['desc']).where(compras.ID == idnota).execute()

                nf = notafiscal.select().where(notafiscal.ID == idnota)    
                flash('Alterado com sucesso')
        
            except:
                flash('Erro ao alterar Compra')
            return redirect('/compras/form/'+str(idnota))
        nf = notafiscal.select().where(compras.ID == idnota)
        return render_template("Form.html", content=nf[0], TableCol=Keys, TableLen = len(Keys), table='notafiscal' , edit=True, id=idnota, active1="",active2="", active3="active", active4="")
    if request.method == 'POST':
      #  try:
            data = dict(request.form)
           
            try:
                data['numero_nf'] = int(data['numero_nf'])
            except:
                data['numero_nf']= 0
                flash('Erro ao cadastrar Numero')
            try:
                data['valor_nf'] = float(data['valor'])
            except:
                data['valor_nf'] = 0.00
                flash('Erro ao cadastrar Valor')

            notafiscal.create(
                    numero_nf=data['numero_nf'], 
                    data_nf=data['data_nf'], valor_nf=data['valor_nf'],  
                    desc= data['desc'])

            idnf = notafiscal.select(fn.MAX(compras.ID)).scalar()
            flash('Cadastrado com sucesso')
            return redirect('/compras/form/'+str(idnf))
     #   except:
     #       flash('Erro ao cadastrar campo(s)')
    return render_template("Form.html", TableCol=Keys, TableLen = len(Keys), table='notafiscal', edit=False, active1="",active2="", active3="active", active4="")

@app.route('/ponto/form/fim/<int:idponto>', methods=['POST', 'GET'])
@login_required
def fim(idponto):
    if not idponto:
        flash('Ponto não encontrada!')
        return redirect('/ponto/form/')
    ponto.update(fim=datetime.datetime.now().strftime('%H:%M:%S')).where(ponto.id == idponto).execute()
    flash('finalizado com successo')
    return redirect('/ponto/form/'+str(idponto))

@app.route('/ponto/form/inicio/', methods=['POST', 'GET'])
@login_required
@employeeLevel
def inicio():
    if request.method == 'POST':
        try:
            data = dict(request.form)
            if not request.form['cod_func'] or request.form['cod_func'] == 0:
                flash('Selecione colaborador')
                return redirect('/ponto/form/')
            desc = data['desc']
            ponto.create(inicio=datetime.datetime.now().strftime('%H:%M:%S') ,desc=desc ,data=datetime.datetime.now().strftime('%Y-%m-%d'), cod_func=data['cod_func'])
        
            idpontonew = ponto.select(fn.MAX(ponto.id)).scalar()
            flash('Ponto Iniciado com successo')
            return redirect('/ponto/form/'+str(idpontonew))
        except:
            flash('Erro ao iniciar ponto. Verifique os campos.')
            return redirect('/ponto/form/')
    return redirect('/ponto/form/')



@app.route('/item/form/', defaults={'iditem': ''}, methods=['POST', 'GET'])
@app.route('/item/form/<int:iditem>', methods=['POST', 'GET'])
@login_required
@employeeLevel
def items(iditem):
    Keys = list(item._meta.fields.keys())
    if iditem != '':
        if request.method == 'GET':
            try:
                materials = Material.select(Material.nome, Material.ID)
                iteminfo = item.select().where(item.id == iditem)
                itempage = page('item', content=iteminfo[0], edit=True, select=materials)
                return itempage.render()
            except:
                return redirect('/item/form/')
        elif request.method == 'POST':
            try:
                item.update(descricao= request.form['descricao'], codigo = request.form['codigo'], material=request.form['material'], esp1=request.form['esp1'], esp2= request.form['esp2'],esp3=request.form['esp3']).where(item.id == iditem).execute()
                return redirect('/item/form/'+str(iditem))
            except:
                return redirect('/item/form/'+str(iditem))
    
    if request.method == 'POST':
        item.create(descricao= request.form['descricao'], codigo = request.form['codigo'], material=request.form['material'], esp1=request.form['esp1'], esp2= request.form['esp2'],esp3=request.form['esp3'])
        itemidnew = item.select(fn.MAX(item.id)).scalar()
        return redirect('/item/form/'+str(itemidnew))
    materials = Material.select(Material.nome, Material.ID)
    itempage = page('item' , select=materials)
    return itempage.render()
    
@app.route('/ponto/form/', defaults={'idponto': ''}, methods=['POST', 'GET'])
@app.route('/ponto/form/<int:idponto>', methods=['POST', 'GET'])
@login_required
@employeeLevel
def pontocad(idponto):
    Keys = list(ponto._meta.fields.keys())
    allcol = funcionarios.select(funcionarios.id, funcionarios.nome)
    if idponto != '':
        pontohora = list(ponto.select(ponto, funcionarios.id, funcionarios.nome).from_(ponto, funcionarios).where(ponto.id == idponto).dicts())
        if not pontohora:
            flash('Ponto Não Encontrado')
            return redirect('/ponto/form/')
        if request.method == 'POST':
            data = dict(request.form)
            try:
                try:   
                    data['data'] = datetime.datetime.strptime(data['data'], '%d/%m/%Y').strftime('%Y-%m-%d')    
                except:
                    data['data'] = datetime.datetime.now().strftime('%d/%m/%Y')
                    flash('Data atual cadastrada')
                try:
                    data['cod_func'] = int(data['cod_func'])
                except:
                    data['cod_func'] = 0
                    flash('Erro ao alterar Colaborador')
                try:
                    data['hora'] = datetime.datetime.strptime(data['hora'], '%H:%M').strftime('%H')
                except:
                    data['hora'] = datetime.datetime.now().strftime('%H:%M')
                #print()
                #print(data['data'])
                #print()
                #print(data['hora'])
                ponto.update(
                    cod_func=request.form['cod_func'], 
                    data=data['data'], hora=data['hora'],  
                    desc= data['desc']).where(ponto.id == idponto).execute()

                #nf = notafiscal.select().where(notafiscal.ID == idnota)    
                flash('Alterado com sucesso')
        
            except:
                flash('Erro ao alterar Ponto')
            return redirect('/ponto/form/'+str(idponto))

        try:
            pontohora[0]['data'] = pontohora[0]['data'].strftime('%d/%m/%Y')
        except:
            pass
        #pontohora[0]['hora'] = datetime.datetime.strptime(pontohora[0]['hora'] , '%Y-%m-%d').strftime('%d/%m/%Y')
        
        return render_template("Form.html", content=pontohora[0], clients = allcol, cliLen= len(allcol), cliCol='cod_func', TableCol=Keys, TableLen = len(Keys), table='ponto' , edit=True, id=idponto,active1="",active2="", active3="active", active4="")
    if request.method == 'POST':
      #  try:
            data = dict(request.form)
            
            try:
                data['data'] = datetime.datetime.strptime(data['data'], '%d/%m/%Y').strftime('%d/%m/%Y')    
            except:
                data['data'] = datetime.datetime.now().strftime('%d/%m/%Y')
                flash('Data atual cadastrada')
            try:
                data['cod_func'] = int(data['cod_func'])
                    
            except:
                data['cod_func'] = 0
                flash('Erro ao alterar Colaborador')
            try:
                data['hora'] = datetime.datetime.strptime(data['hora'], '%H:%M').strftime('%H:%M:%S')
            except:
                data['hora'] = datetime.datetime.now().strftime('%H')

            ponto.create(
                cod_func=request.form['cod_func'], 
                data=data['data'], hora=data['hora'],  
                desc= request.form['desc'])


            idpontonew = ponto.select(fn.MAX(ponto.id)).scalar()
            flash('Cadastrado com sucesso')
            return redirect('/ponto/form/'+str(idpontonew))
     #   except:
     #       flash('Erro ao cadastrar campo(s)')
    return render_template("Form.html", TableCol=Keys, TableLen = len(Keys), clients=allcol, cliLen= len(allcol), cliCol='cod_func', data=datetime.datetime.now().strftime('%d/%m/%Y'), table='ponto', edit=False, active1="",active2="", active3="active", active4="")


@app.route('/pedidos/form/', defaults={'idpedido': ''}, methods=['POST', 'GET'])
@app.route('/pedidos/form/<int:idpedido>', methods=['POST', 'GET'])
@login_required
@managerLevel
def pedido(idpedido):
    clients = Clientes.select(Clientes.nome, Clientes.ID)
    ferramentas = Ferramenta.select(Ferramenta.Ferramenta, Ferramenta.ID)
    if idpedido != '':
        if request.method == 'GET':
           
            content = Pedidos.select().where(Pedidos.id == idpedido)
            pagePedido = page('Pedidos', content[0], select=clients, select2=ferramentas,edit=True)
            return pagePedido.render()
        elif request.method == 'POST':
            Pedidos.update(numero = request.form['numero'], ano = request.form['ano'], id_cliente=request.form['id_cliente'], id_ferramenta= request.form['id_ferramenta'], especificacao= request.form['especificacao'], desenho=request.form['desenho'], unidade=request.form['unidade'], qnt= request.form['qnt'], preco=request.form['preco'],  data_entrada=datetime.datetime.strptime(request.form['data_entrada'], '%Y-%m-%d'), prazo=datetime.datetime.strptime(request.form['prazo'], '%Y-%m-%d'), qnt_acabada=request.form['qnt_acabada'], data_acabamento=request.form['data_acabamento'], pedido_cliente=request.form['pedido_cliente'], numero_os=request.form['numero_os'] ).where(Pedidos.ID == idpedido).execute()
            flash("Alterado com Sucesso")
            return redirect('/pedido/form/'+ str(idpedido))
    if request.method == 'POST':
          Pedidos.create(numero = request.form['numero'], ano = request.form['ano'], id_cliente=request.form['id_cliente'], id_ferramenta= request.form['id_ferramenta'], especificacao= request.form['especificacao'], desenho=request.form['desenho'], unidade=request.form['unidade'], qnt= request.form['qnt'], preco=request.form['preco'],  data_entrada=datetime.datetime.strptime(request.form['data_entrada'], '%Y-%m-%d'), prazo=datetime.datetime.strptime(request.form['prazo'], '%Y-%m-%d'), qnt_acabada=request.form['qnt_acabada'], data_acabamento=request.form['data_acabamento'], pedido_cliente=request.form['pedido_cliente'], numero_os=request.form['numero_os'] )
          idfuncnew = Pedidos.select(fn.MAX(Pedidos.ID)).scalar()
          flash("Cadastrado com Sucesso")
          return redirect('/pedido/form/'+ str(idfuncnew))
    pagePedido = page('Pedidos', select=clients, select2=ferramentas)
    return pagePedido.render()
@app.route('/funcionarios/form/', defaults={'idfunc': ''}, methods=['POST', 'GET'])
@app.route('/funcionarios/form/<int:idfunc>', methods=['POST', 'GET'])
@login_required
@adminLevel
def func(idfunc):
    if idfunc != '':
        if request.method == 'GET':
            content = funcionarios.select().where(funcionarios.id == idfunc)
            pagefunc = page('funcionarios', content[0], edit=True)
            return pagefunc.render()
        elif request.method == 'POST':
            funcionarios.update(funcionario = request.form['funcionario'], nome = request.form['nome'], senha=request.form['senha']).where(funcionarios.id == idfunc).execute()
            flash("Alterado com Sucesso")
            return redirect('/funcionarios/form/'+ str(idfunc))
        
    if request.method == 'POST':
          funcionarios.create(funcionario = request.form['funcionario'], nome = request.form['nome'], senha=request.form['senha'])
          idfuncnew = funcionarios.select(fn.MAX(funcionarios.id)).scalar()
          flash("Cadastrado com Sucesso")
          return redirect('/funcionarios/form/'+ str(idfuncnew))
    pagefunc = page('funcionarios')
    return pagefunc.render()


@app.route('/processos/form/', defaults={'idproc': ''}, methods=['POST', 'GET'])
@app.route('/processos/form/<int:idproc>', methods=['POST', 'GET'])
@login_required
@adminLevel
def processosOs(idproc):
    if idproc != '':
        if request.method == 'GET':
            content = processos.select().where(processos.ID == idproc)
            if not content:
                flash('Não Encontrada!')
                return redirect('/processos/form/')
            pagefunc = page('processos', content[0], edit=True)
            return pagefunc.render()
        elif request.method == 'POST':
            processos.update(Nome = request.form['Nome'], Tempo_Objetivo = request.form['Tempo_Objetivo']).where(processos.ID == idproc).execute()
            flash("Alterado com Sucesso")
            return redirect('/processos/form/'+ str(idproc))

    if request.method == 'POST':
          processos.create(Nome = request.form['Nome'], Tempo_Objetivo = request.form['Tempo_Objetivo'])
          idfuncnew = processos.select(fn.MAX(processos.ID)).scalar()
          flash("Cadastrado com Sucesso")
          return redirect('/processos/form/'+ str(idfuncnew))
    pagefunc = page('processos')
    return pagefunc.render()


@app.route('/<string:table>', methods=['GET'])
@login_required
def renderTable(table):
    tablefinan = ['caixa', 'numero_pedidos', 'fornecedores', 'constasapagar', 'constasareceber', 'compras']
    tablefunc = ['ponto']
    tablegeren = ['cadastro_os', 'fornecedores', 'numero_pedidos', 'compras', 'material', 'estoque']
    tok = jwt.decode(session.get('token'), os.environ['SECRET_KEY'], algorithms=['HS256'])
    if tok['level'] == 4:
        return render_list(table)
    if tok['level'] == 3 and table.lower() in tablefinan :
        return render_list(table)
    elif tok['level'] == 2 and table.lower() in tablegeren:
        return render_list(table)
    elif tok['level'] == 1 and table.lower() in tablefunc:
        return render_list(table)
    else:
        return redirect('/')
   
@app.route('/historico_os/form/', defaults={'idhist': ''}, methods=['POST', 'GET'])
@app.route('/historico_os/form/<int:idhist>', methods=['POST', 'GET'])
@login_required
def histform(idhist):
    allcol = processos.select(processos.ID, processos.Nome)
    allos = Cadastro_OS.select(Cadastro_OS.Id, Cadastro_OS.Numero_Os)
    if idhist != '':
       if request.method == 'POST':
           try:
              if request.form['data'] != '':
                 data  = datetime.datetime.strptime(str(request.form['data']), '%d/%m/%Y').strftime('%Y-%m-%d')
           except:
                pass
           Historico_os.update(id_proc = request.form['id_proc'], id_os = request.form['id_os'], inicio = request.form['inicio'], fim= request.form['fim'], periodo=request.form['periodo'], data=data, qtd=request.form['qtd']).where(Historico_os.ID == idhist).execute()  
       
       hist_os =  list(Historico_os.select().where(Historico_os.ID == idhist).dicts())
       
       if hist_os[0]['data'] != '':
           
          hist_os[0]['data'] = hist_os[0]['data'].strftime('%d/%m/%Y')
          
       pageedit = page('Historico_os', content=hist_os[0], edit=True, select=allcol, select2=allos)
       return pageedit.render()
       #return render_template('Form.html', clients = allcol, cliLen= len(allcol), content=)
    
    if request.method == 'POST':
       try:
          if request.form['data'] != '':
            data  = datetime.datetime.strptime(str(request.form['data']), '%d/%m/%Y').strftime('%Y-%m-%d')
       except:
          pass
          Historico_os.create(id_proc = request.form['id_proc'], id_os = request.form['id_os'], inicio = request.form['inicio'], fim= request.form['fim'], periodo=request.form['periodo'], data=data, qtd=request.form['qtd'])
          idfuncnew = Historico_os.select(fn.MAX(Historico_os.ID)).scalar()
          flash("Cadastrado com Sucesso")
          return redirect('/processos/form/'+ str(idfuncnew))

    pagenew = page('Historico_os', edit=False, select=allcol, select2=allos)
    return pagenew.render()


@app.route('/delete/table=<string:col>&id=<int:idtab>', methods=['GET','POST'])
@login_required
def deleterow(col, idtab):
    if col != '' and idtab >= 0:
        try:
            try:    
                str_to_class(col).delete().where(str_to_class(col).id == idtab).execute()
                flash('Deletado com sucesso!')
                return redirect('/'+str(col.lower())+'/form/')
            except:
                pass
            try:
                str_to_class(col.capitalize()).delete().where(str_to_class(col.capitalize()).id == idtab).execute()
                flash('Deletado com sucesso!')
                return redirect('/'+str(col.lower())+'/form/')
            except:
                raise Exception
        except:
            pass
        try:
            try:    
                str_to_class(col).delete().where(str_to_class(col).Id == idtab).execute()
                flash('Deletado com sucesso!')
                return redirect('/'+str(col.lower())+'/form/')
            except:
                pass
            try:
                str_to_class(col.capitalize()).delete().where(str_to_class(col.capitalize()).Id == idtab).execute()
                flash('Deletado com sucesso!')
                return redirect('/'+str(col.lower())+'/form/')
            except:
                raise Exception
        except:
            pass

        try:
            try:    
                str_to_class(col).delete().where(str_to_class(col).ID == idtab).execute()
                flash('Deletado com sucesso!')
                return redirect('/'+str(col.lower())+'/form/')
            except:
                pass
            try:
                str_to_class(col.capitalize()).delete().where(str_to_class(col.capitalize()).ID == idtab).execute()
                flash('Deletado com sucesso!')
                return redirect('/'+str(col.lower())+'/form/')
            except:
                raise Exception
        except:
            flash('Erro ao deletar.')
            return redirect('/'+str(col.lower())+'/form/'+ str(idtab))
    #print(idtab)

@app.route('/redirect/<int:n_os>', methods=['GET'])
def redirect_num(n_os):
    try:
        idos = list(Cadastro_OS.select(Cadastro_OS.Id).where(Cadastro_OS.Numero_Os == n_os).dicts())
        #print(idos[0]['Id'])
        return redirect('/os/form/'+ str(idos[0]['Id']))
    except:
        return redirect('#')

@app.route('/linha/form/', defaults={'idlinha': ''}, methods=['POST', 'GET'])
@app.route('/linha/form/<int:idlinha>', methods=['POST', 'GET'])
@login_required
def linha_os(idlinha):
    if idlinha!='':
        content = linha.select().where(linha.id==idlinha)
        if request.method == 'POST':
            try:
                num = int(request.form['numero_inicial'])
            except:
                num = 0
            content.update(nome= request.form['nome'], numero_inicial = num).execute()
        pageLinha = page('linha', content=content[0])
        pageLinha.render()
    if request.method == 'POST' and request.form:
        try:
            num = int(request.form['numero_inicial'])
        except:
            num = 0
        linha.create(nome= request.form['nome'], numero_inicial = num).execute()
    pageLinha = page('linha')
    return pageLinha.render()

@app.errorhandler(404) 
def invalid_route(e): 
    return underdev()















"""

*** API ROUTES ***

"""

@app.route('/app/api/login', methods=['POST'])
@cross_origin()
def longlogin():
    obj = json.loads(request.data)
    rows = usuarios.select(usuarios.ds_senha).where(usuarios.ds_login == obj['username'])
     #rows = db.execute('SELECT ds_senha FROM usuarios WHERE  ds_login = ?', obj['username'])
    rows = [model_to_dict(row) for row in rows]
        #obj = json.loads(request.data)
     ##print(obj['username'])
       
    password = obj['password']
    #print(obj['password'])
    
    if check_password_hash(rows[0]["ds_senha"], password) or rows[0]["ds_senha"] == password:
                
        token = jwt.encode({'user': obj['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, os.environ['SECRET_KEY'])
            # request.headers['authorization'] = token.decode('UTF-8')
        return make_response(jsonify({'token': token.decode('UTF-8')}))
        
    return jsonify('Not found')
        
    

@app.route('/api/login', methods=['POST'])
def log():
   
    obj = json.loads(request.data)
    try:
        obj = (obj['data'])
    except:
        pass
        
    #print(obj)
    #print(obj['username'])
    rows = usuarios.select(usuarios.ds_senha).where(usuarios.ds_login == obj['username'])
     #rows = db.execute('SELECT ds_senha FROM usuarios WHERE  ds_login = ?', obj['username'])
    rows = [model_to_dict(row) for row in rows]
        #obj = json.loads(request.data)
     ##print(obj['username'])
       
    password = obj['password']
    #print(obj['password'])
    #print(rows[0]["ds_senha"])
    
    if check_password_hash(rows[0]["ds_senha"], password) or rows[0]["ds_senha"] == password:
                
        token = jwt.encode({'user': obj['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, os.environ['SECRET_KEY'])
            # request.headers['authorization'] = token.decode('UTF-8')
        resp = make_response(jsonify({'token': token.decode('UTF-8')}))
            # resp.headers['Origin'] = 
        return resp
        
    return jsonify('Not found')
        
  
@app.route('/os/all')
@login_required
def all_api():
    rows = Cadastro_OS.select()
    rows = [model_to_dict(row) for row in rows]
    return rows



@app.route('/api/os/<int:osid>', methods=['POST', 'GET'])
@auth_required
@cross_origin()
def osApi(osid):
    try:
        rows = Cadastro_OS.select().where(Cadastro_OS.Id == osid)
        rows = [model_to_dict(row) for row in rows]
        #rows = db.execute('SELECT * FROM Cadastro_OS WHERE Id = '+ str(osid))
        if not rows:
            return jsonify('Not found')
        if request.method == 'POST':
             obj = json.loads(request.data)
             try:
                  updateData(obj, 'Cadastro_OS', 'Id', osid)
                  return jsonify('Updated')
             except:
                 return jsonify('Error')
        return jsonify(rows)
    except:
        return jsonify('not-found')
 
@app.route('/api/os/limit=<int:limit>', methods=['GET', 'POST'])
@auth_required
def osApiall(limit):
  #  try:
        rows = list(Cadastro_OS.select(Cadastro_OS, Clientes.nome).from_(Cadastro_OS, Clientes).where(Cadastro_OS.Id_Cliente == Clientes.ID).order_by(Cadastro_OS.Numero_Os.desc()).limit(int(limit)).dicts())
        ##print()
       # #print(rows)
        #rows = [model_to_dict(row) for row in rows]
        #stmt = "SELECT c.ID, c.nome, o.Tipo, o.Especificacao, o.Prazo, o.Numero_Os, o.Id_Cliente, o.Id, o.Data FROM Clientes c, Cadastro_OS o WHERE c.ID=o.Id_Cliente ORDER BY o.Numero_Os DESC LIMIT " + str(limit)
        if request.method == 'GET':
            #db.execute('SELECT * FROM Cadastro_OS ORDER BY Id DESC LIMIT '+ str(limit))
            

            return jsonify(list(rows))
        elif request.method == 'POST':
          #  try:
                obj = json.loads(request.data)
                insertData(obj, 'Cadastro_OS')
                return jsonify('Created-Successfully')
            #except:
              #  return jsonify('Create-Error')
        
 #   except:
     #   return jsonify('Not found')

@app.route('/api/os/q=<string:query>', methods=['GET', 'POST'])
@auth_required
def osApiSearch(query):
  #  try:
        if len(query) < 2:
         #   rows = list(Cadastro_OS.select(Cadastro_OS, Clientes.nome).from_(Cadastro_OS, Clientes).where(Cadastro_OS.Especificacao.contains(query), Cadastro_OS.Id_Cliente == Clientes.ID).order_by(Cadastro_OS.Numero_Os.desc()).limit(int(limit)).dicts())
            rows = list(Cadastro_OS.select(Cadastro_OS, Clientes.nome).from_(Cadastro_OS, Clientes).where(Cadastro_OS.Especificacao.contains(query), Cadastro_OS.Id_Cliente == Clientes.ID).order_by(Cadastro_OS.Numero_Os.desc()).limit(200).dicts())
        else:
            rows = list(Cadastro_OS.select(Cadastro_OS, Clientes.nome).from_(Cadastro_OS, Clientes).where(Cadastro_OS.Especificacao.contains(query), Cadastro_OS.Id_Cliente == Clientes.ID).order_by(Cadastro_OS.Numero_Os.desc()).dicts())
    
        #stmt = "SELECT c.ID, c.nome, o.Tipo, o.Prazo, o.Especificacao, o.Numero_Os, o.Id_Cliente, o.Id, o.Data FROM Clientes c, Cadastro_OS o WHERE c.ID=o.Id_Cliente AND o.Especificacao LIKE '%" + str(query) + "%' ORDER BY o.Numero_Os DESC "
        
     #   if limit > 0:
     #       stmt += " LIMIT " + str(limit)
        if request.method == 'GET':
            #rows = db.execute(stmt)
            #db.execute('SELECT * FROM Cadastro_OS ORDER BY Id DESC LIMIT '+ str(limit))
          
            return jsonify(rows)
        elif request.method == 'POST':
          #  try:
                obj = json.loads(request.data)
                insertData(obj, 'Cadastro_OS')
                return jsonify('Created-Successfully')
            #except:
              #  return jsonify('Create-Error')
        
 #   except:
     #   return jsonify('Not found')



@app.route('/api/os/new')
@auth_required
def osApiNum():
    try:
          os_num = Cadastro_OS.select(fn.MAX(Cadastro_OS.Numero_Os)).scalar()
          os_num = int(os_num) + 1
          return jsonify(os_num)
    except:
        return jsonify('Error')

@app.route('/api/clientes', methods=['GET', 'POST'])
@auth_required
def allClientes():
    clients = list(Clientes.select().dicts())
    #clients = [model_to_dict(client) for client in clients]
    return jsonify(clients)

@cross_origin(origin='*',headers=['Content- Type','Authorization', 'authorization'])
@app.route('/api/processos/inicio', methods=['POST'])
@auth_required
def inicioProcesso():
    try:
        obj = json.loads(request.data)
        if 'http' in obj['osid'][0]["url"]:
            jtok = obj['osid'][0]["url"][37:]
        else:
            jtok = obj['osid'][0]["url"] 
        #print(jtok)
        objtok = jwt.decode(jtok, os.environ['SECRET_KEY'], algorithms=['HS256'])
        osid = objtok['osid']
        horario = obj['horario']
        idproc = obj['idProc']
        qtd = obj['qtd']
        altos = Cadastro_OS.select().where(Cadastro_OS.Id == osid).get()
        altos.STATUS = idproc
        altos.save()

        osproc = Historico_os.select().where((Historico_os.id_os == osid) & (Historico_os.id_proc == idproc) & (Historico_os.inicio != '') )
        if osproc:
            osproc = osproc.get()
            if osproc.fim == None or osproc.fim == '':
                return jsonify("Período do processo não finalizado!")

        osproc = Historico_os.select().where((Historico_os.id_os == osid) &
        (Historico_os.id_proc == idproc) & (Historico_os.inicio != '') & (Historico_os.fim != None) )
        if (osproc):
            periodo = Historico_os.select(fn.MAX(Historico_os.periodo)).where((Historico_os.id_os == osid) & (Historico_os.id_proc == idproc)).scalar()
            #print(periodo)
            if not periodo:
                periodo = 1
            else:
                periodo = periodo + 1
            Historico_os.create(id_proc=idproc, id_os=osid, inicio=horario, periodo=periodo, data=date.today(), qtd=qtd)
            return jsonify("Periodo número "+str(periodo)+" do processo já iniciado!")    
        
    
        Historico_os.create(id_proc=idproc, id_os=osid, inicio=horario, periodo=1, data=date.today(), qtd=qtd)    
        return jsonify("Período do processo iniciado com Sucesso!")
    except:
        return jsonify("O.S Inválida")
        
@cross_origin(origin='*',headers=['Content- Type','Authorization', 'authorization'])
@app.route('/api/processos', methods=['GET'])
@auth_required
def allProcesso():
    if request.method == 'GET':
        process_list = processos.select()
        process_list = [model_to_dict(processo) for processo in process_list]
        return jsonify(process_list)

@cross_origin(origin='*',headers=['Content- Type','Authorization', 'authorization'])
@app.route('/api/processos/fim', methods=['POST'])
@auth_required
def fimProcesso():
    
    obj = json.loads(request.data)
            
            #jtok = re.sub(r'^https?:\/\/.*[\r\n]*', '', obj['osid'][0]["url"])
    if 'http' in obj['osid'][0]["url"]:
        jtok = obj['osid'][0]["url"][37:]
    else:
        jtok = obj['osid'][0]["url"] 
        #print(jtok)
            
    objtok = jwt.decode(jtok, os.environ['SECRET_KEY'], algorithms=['HS256'])
    osid = objtok['osid']
    horario = obj['horario']
    idproc = obj['idProc']
    
    periodo = Historico_os.select(fn.MAX(Historico_os.periodo)).where((Historico_os.id_os == osid)  &
    (Historico_os.id_proc == idproc)).scalar()
    if not periodo:
        periodo = 1
    althistos = Historico_os.select().where( 
    (Historico_os.id_os == osid) &
    (Historico_os.id_proc == idproc) &
    (Historico_os.periodo == periodo) & (Historico_os.fim == None))
    if (althistos):
        althistos = althistos.get()
        althistos.fim = horario
        althistos.save()
        return jsonify("Período "+str(periodo)+" Finalizado!")
    return jsonify("Periodo do processo não iniciado!")
    #except:
       #return jsonify("O.S Inválida!") 



@app.route('/api/clientes/id=<int:id>', methods=['GET', 'POST'])
@auth_required
def IdClientes(id):
    #stmt = "SELECT ID, nome FROM Clientes ORDER BY nome ASC"
    res = Clientes.select(Clientes.ID, Clientes.nome).where(Clientes.ID == id).order_by(Clientes.ID.asc())
    return jsonify(model_to_dict(res))


@app.route('/api/clientes/', defaults={'query': 'none'}, methods=['POST', 'GET'])
@app.route('/api/clientes/q=<string:query>', methods=['POST', 'GET'])
@auth_required
def nome(query):
    #stmt = "SELECT ID, nome FROM Clientes ORDER BY nome ASC"
    res = list(Clientes.select().where(Clientes.nome.contains(query)).order_by(Clientes.ID.asc()).dicts())
    #res = [model_to_dict(row) for row in res]
    return jsonify(res)

@app.route('/api/clientes/limit=<int:limit>', methods=['GET','POST'])
@auth_required
def cliLimit(limit):
    res = list(Clientes.select().order_by(Clientes.ID.asc()).limit(int(limit)).dicts())
    #res = [model_to_dict(row) for row in res]
    return jsonify(res)


@app.route('/api/estoque/limit=<int:limit>', methods=['GET','POST'])
@auth_required
def allEstoque(limit):
   
    if request.method == 'GET':
        rows = list(Estoque.select(Estoque, Clientes.nome).from_(Estoque, Clientes).where(Estoque.id_cliente == Clientes.ID).order_by(Estoque.qt.desc()).dicts())
        #print(rows)
        return jsonify(rows)
    elif request.method == 'POST' and request.data:
          #  try:
        obj = json.loads(request.data)
        insertData(obj, 'Estoque')
        return jsonify('Item-criado')
    else:
        return jsonify('UNAUTHORIZED')

@app.route('/api/estoque/q=<string:query>&col=<string:col>', methods=['GET'])
@auth_required
def queryEstoque(query, col):
    rows = Estoque.select(Estoque, Clientes.nome).from_(Estoque, Clientes).where(Estoque.id_cliente == Clientes.ID, Estoque[col].contains(query)).order_by(Estoque.qt.desc())
    #stmt = "SELECT e.*, c.nome FROM Estoque e, Clientes c WHERE c.ID = e.id_cliente AND "+ col + "=" + query +" ORDER BY e.ID DESC"
    ##print(stmt)
    #rows = db.execute(stmt)  
    return jsonify(rows)


@app.route('/api/item/allitems', methods=['GET'])
@auth_required
def getItems():
    rows = list(item.select(item, Material.nome).from_(item, Material).where(item.cod_mat == Material.ID).order_by(item.id.desc()).dicts())
    return jsonify(rows)


@app.route('/api/item/<int:itemid>', methods=['GET', 'POST'])
@auth_required
def alterItems():
    if request.method == 'GET':
        rows = list(item.select().where(item.id== iditem).dicts())
        return jsonify(rows)
        
    elif request.method == 'POST':
        obj = json.loads(request.data)
        alterItem = item.select().where(item.id == iditem)
        alterItem['descricao'] = obj['descricao']
        alterItem['cod_mat'] = obj['cod_mat']
        alterItem.save()
        return jsonify('Atualizado')

@app.route('/api/item/', methods=['POST'])
@auth_required
def createItem():
    obj = json.loads(request.data)
    item.create(descricao=obj['descricao'], cod_mat=obj['cod_mat'])
    

    

    





@app.route('/api/progress/<int:n_os>', methods=['GET'])
@auth_required
def progress(n_os):
    return os_em_andamento(n_os)

@app.route('/api/progress/allos', methods=['GET'])
@auth_required
def osinprogress():
    os = os_em_historico()
    return jsonify(os)





if __name__ == "__main__" :
     app.run(debug=True)
     socketio.run(app, debug=True)