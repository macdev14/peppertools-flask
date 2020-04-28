
from helper import *
from flask import Flask, redirect,render_template, request, session
from flask_session.__init__ import Session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import sys
from cs50 import SQL
import datetime

db = SQL("sqlite:///peppertools.db")

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

