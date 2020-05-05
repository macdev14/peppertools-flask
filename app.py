
from helper import *
from api import *
from flask import Flask, redirect,render_template, request, session, flash
from flask_session.__init__ import Session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import sys
import json
from jinja2 import Undefined
from cs50 import SQL
import datetime

db = SQL("sqlite:///peppertools.db")
JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
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
def os():
    os = getData("key","*", "Cadastro_Os","limit","Numero_os") 
    os_val = getData("val","*", "Cadastro_Os", "limit", "Numero_os")
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
    if request.method == 'POST':
        data = dict(request.form)
        try:
            data['Numero_Os'] = int(data['Numero_Os'])
            data['Id_Cliente'] = int(data['Id_Cliente'])
            data['Numero_Nf'] = int(data['Numero_Nf'])
            data['Numero_Pedido'] = int(data['Numero_Pedido'])
            data['Quantidade'] = int(data['Quantidade'])
            data['Id'] = int(data['Id'])
        except:
            pass
        
        updateData(data, 'Cadastro_OS', 'Numero_Os', osid)
        flash('O.S alterada com sucesso')
        return redirect('/os/form/'+str(osid))
    clients = getClient()
    os_num = getOs()
    os = getOs(osid)
    print(dict(os[0]))
    field = os[0]
    print(field['Numero_Os'])
    x = datetime.datetime.now()
    date = x.strftime("%d/%m/%Y")
    return render_template('os_gen.html', clients = clients, clients_len = len(clients), os_num = int(os_num), field = field , data = date)

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
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Usuário necessário")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Senha necessária")
            return redirect("/register")

        if request.form.get("password") != request.form.get("password-confirm"):
            flash("Senhas não coincidem")
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
                return redirect("/")
            except:
                flash("Could not register user")
                return redirect("/register")
    return render_template("register.html")
  

