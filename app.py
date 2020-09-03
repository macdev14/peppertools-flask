from helper import *
from api import *
from flask_qrcode import QRcode 
from flask import Flask, redirect,render_template, request, session, flash, jsonify, make_response
from flask_session.__init__ import Session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import sys
import jwt
import json
from jinja2 import Undefined
from cs50 import SQL
import datetime
from flask_ssl import *

db = SQL("sqlite:///peppertools.db")
JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }
app = Flask(__name__)

app.config["SECRET_KEY"] = 'caf3cc4546725599c99158599d443fc815bd137b73b0b69bc804f3ba483aeaa224c75a2b3fc1f35eccfdfef6cdd01858450435ef6daed0c49bf01fbe1e7b3b79'
QRcode(app)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers['Access-Control-Allow-Origin'] = '*'
    #response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
@login_required
def index():
    return render_template("layout.html", title= "Inicio", active1="active",active2="", active3="", active4="")


@app.route('/clientes')
@login_required
def clientes():
    clientes = getData("key","*", "Clientes","","")
    clientes_val = getData("val","*", "Clientes","","")
    clientes_len = len(clientes)
    val_len = len(clientes_val)
    #return getClientes("key","*")
    return render_template("clientes.html", title="Clientes", clientes=clientes, clientes_val = clientes_val, clientes_len = clientes_len, 
                            val_len = val_len, active1="",active2="", active3="active", active4="")


@app.route('/clientes/buscar')
@login_required
def search():
    return underdev()


@app.route('/clientes/editar', methods=["GET", "POST"])
@login_required
def editar():
    if request.method == 'GET':
        return redirect("/clientes")
    else:
        clientes = getData("key","*", "Clientes")
        id = request.form.get("id")
        return render_template("client_edit.html", clientes=clientes, id=id, active1="",active2="", active3="active", active4="")


@app.route("/os")
@login_required
def osAll():
    os = getData("key","*", "Cadastro_Os",True,"Numero_os") 
    os_val = getData("val","*", "Cadastro_Os", True, "Numero_os")
    os_len = len(os) 
    val_len = len(os_val)
    return render_template("os.html", os=os, os_val= os_val, os_len=os_len, val_len=val_len, active1="",active2="", active3="", active4="active")     


@app.route("/os/imprimir")
@login_required
def print1():
    #return render_template("imprimir_os.html", title= "Inicio", active1="active",active2="", active3="", active4="active")
    return underdev()


@app.route("/os/buscar")
@login_required
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
    x = datetime.datetime.now()
    date = x.strftime("%d/%m/%Y")
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        return login_user(user, password)
    else:    
        return render_template('login.html', date = date)


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/login')


@app.route("/os/total")
@login_required
def all():
    return getNumber()


@app.route('/os/form/', methods=["POST", "GET"])
@login_required
def new_os():
    clients = db.execute('SELECT DISTINCT Clientes.ID, nome FROM Cadastro_OS, Clientes WHERE Cadastro_OS.id_cliente = Clientes.ID')
    x = datetime.datetime.now()
    date = x.strftime("%d/%m/%Y")
    os_num = db.execute('SELECT MAX(Numero_Os) AS num_os FROM Cadastro_OS')
    os_num = int(os_num[0]['num_os']) + 1
    clients_len = len(clients)
    if request.method == 'POST' and request.form['Id_Cliente'] != str(0):
        print(dict(request.form))
        data = dict(request.form)
       # data = json.loads(data)
        print(insertData(data, 'Cadastro_Os'))
        flash('O.S cadastrada com sucesso')
        return redirect('/os/form/'+ str(data['Id']))
    elif request.method == 'POST':
        flash('Erro ao cadastrar O.S')
        return redirect('/os/form/')
    print(request.form)
    return render_template('os_gen.html', clients = clients, clients_len = clients_len, os_num = os_num, field = '' , data = date)


@app.route('/os/form/<int:osid>', methods = ['POST', 'GET'])
@login_required
def os_edit(osid):
    try:
        osid2 = session['osid']
    except:
        osid2 =  osid    
    if request.method == 'POST':
        data = dict(request.form)
        try:
            data['Numero_Os'] = int(data['Numero_Os'])
            data['Id_Cliente'] = int(data['Id_Cliente'])
            data['Numero_Nf'] = int(data['Numero_Nf'])
            data['Numero_Pedido'] = int(data['Numero_Pedido'])
            data['Quantidade'] = int(data['Quantidade'])
            data['Id'] = int(data['Id'])
            data['Data'] = datetime.datetime.strptime(checkDate(data['Data']), '%m/%d/%y').strftime('%d/%m/%Y')
            data['Data_Pedido'] = datetime.datetime.strptime(checkDate(data['Data']), '%m/%d/%y').strftime('%d/%m/%Y')
        except:
            pass
        updateData(data, 'Cadastro_OS', 'Numero_Os', osid)
        flash('O.S alterada com sucesso')
        return redirect('/os/form/'+str(osid))
        session['osid'].clear()
    try:
        clients = getClient()
        os_num = getOs()
        os = getOs(osid)
        print(dict(os[0]))
        field = os[0]
        if field['Data_Pedido']:
            field['Data_Pedido'] = checkDate(field['Data_Pedido'])
        field['Data'] = checkDate(field['Data'])
        if field['Prazo']:
            field['Prazo'] = checkDate(field['Prazo'])
        if field['Data_Nf']:
            field['Data_Nf'] = checkDate(field['Data_Nf'])
        print(field['Data'])
        print(field['Numero_Os'])
        x = datetime.datetime.now()
        date = x.strftime("%d/%m/%Y")
        return render_template('os_gen.html', clients = clients, clients_len = len(clients), os_num = int(os_num), field = field , data = date)
    except:
        flash('O.S não encontrada!')
        return redirect('/os/form/')

@app.route('/os/form/delete/<int:osid>', methods = ['POST', 'GET'])
@login_required
def os_del(osid):
    if request.method == 'GET':
        try:
            deleteData('Cadastro_Os', 'Numero_Os', osid)
            flash('O.S deletada com sucesso')
            return redirect('/os/form/')
        except:
            flash('Erro ao deletar O.S')
            return redirect('/os/form/'+str(osid))
    flash('Erro ao deletar O.S')
    return redirect('/os/form/')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if not request.is_secure and app.env != "development":
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code) 
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Usuário inválido.")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Senha inválida")
            return redirect("/register")

        elif not request.form.get("key"):
            flash("Chave inválida")
            return redirect("/register")

        if request.form.get("password") != request.form.get("password-confirm"):
            flash("Senhas não coincidem")
            return redirect("/register")

        if request.form.get("key") != "12@Afiado#45":
            flash("Chave inválida")
            return redirect("/register")

        # Query database for username
        rows = db.execute("SELECT * FROM usuarios WHERE ds_login = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) == 1:
            if check_password_hash(rows[0]["ds_senha"], request.form.get("password")):
                flash("User or password already exists")
                return redirect("/register")
            flash("User or password already exists")
            return redirect("/register")
        else:
            try:
                db.execute('INSERT INTO usuarios(ds_login, ds_senha, nivel) VALUES(:username, :hash, :nivel)', username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")), nivel=3),
                rows = db.execute("SELECT * FROM usuarios WHERE ds_login = :username",
                              username=request.form.get("username"))
                session["user_id"] = rows[0]["ID"]
                session["level"] = rows[0]["nivel"]
                return redirect("/")
            except:
                flash("Could not register user")
                return redirect("/register")
    return render_template("register.html")
  

@app.route('/os/form/print/<int:osid>', methods = ['GET'])
def print_os(osid):
    print(osid)
    if request.method == 'GET':
        os = getOs(osid)
        field = dict(os[0])
        res = getClient(osid)
        print(res)
        qr = "http://peppertools.cf/os/"+str(field['Numero_Os'])
        field['nome'] = res['nome']
        field['Data_digit'] = datetime.datetime.strptime(checkDate(field['Data']), '%d/%m/%Y').strftime('%y')
        field['Data'] = checkDate(field['Data'])
        field['Data_Nf'] = checkDate(field['Data_Nf'])
        field['Data_Pedido'] = checkDate(field['Data_Nf'])
        field['Prazo'] = checkDate(field['Prazo'])
        return render_template("imprimir_os.html", field = field, qr=qr)
        session['osid'] = ''

@app.route('/os/<int:osid>', methods = ['POST', 'GET'])
def access(osid):
    session['osid'] = osid
    @login_required
    def goTo(osid):
        return redirect('form/'+str(osid))
    return goTo(osid)

@app.route('/os/all')
def all_api():
    return getAll()

@app.route('/api/login', methods=['POST'])
def log():
     try:
        obj = json.loads(request.data)
     #print(obj['username'])
        user = obj['username']
        password = obj['password']
        print(obj['password'])
        rows = db.execute('SELECT * FROM usuarios WHERE  ds_login = ?', user)
        #print(rows[0]["ds_senha"])
        if len(rows) == 1 and check_password_hash(rows[0]["ds_senha"], password):
            
            token = jwt.encode({'user': obj['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        # request.headers['authorization'] = token.decode('UTF-8')
            resp = make_response(jsonify({'token': token.decode('UTF-8')}))
          # resp.headers['Origin'] = 
            return resp
        return jsonify('Not found')
     except:       
            return jsonify('Not found')

@app.route('/api/os/<int:osid>', methods=['POST', 'GET'])
@auth_required
def osApi(osid):
    try:
        rows = db.execute('SELECT * FROM Cadastro_OS WHERE Id = '+ str(osid))
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
 
@app.route('/api/os/', methods=['GET', 'POST'])
@auth_required
def osApiall():
  #  try:
        if request.method == 'GET':
            rows = db.execute('SELECT * FROM Cadastro_OS ORDER BY Id')
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
          os_num = db.execute('SELECT MAX(Numero_Os) AS num_os FROM Cadastro_OS')
          os_num = int(os_num[0]['num_os']) + 1
          return jsonify(os_num)
    except:
        return jsonify('Error')




if __name__ == "__main__" :
     app.run(debug=True)