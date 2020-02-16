
from helper import getData
from flask import Flask, redirect,render_template, request, session
from flask_session.__init__ import Session
import sqlite3
import sys


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("layout.html", title= "Inicio", active1="active",active2="", active3="", active4="")

@app.route('/clientes')
def clientes():
    clientes = getData("key","*", "Clientes","","")
    clientes_val = getData("val","*", "Clientes","","")
    clientes_len = len(clientes)
    val_len = len(clientes_val)
    #return getClientes("key","*")
    return render_template("clientes.html", title="Clientes", clientes=clientes, clientes_val = clientes_val, clientes_len = clientes_len, 
                            val_len = val_len, active1="",active2="", active3="active", active4="")

@app.route('/clientes/editar', methods=["GET", "POST"])
def editar():
    if request.method == 'GET':
        return redirect("/clientes")
    else:
        clientes = getData("key","*", "Clientes")
        id = request.form.get("id")
        return render_template("client_edit.html", clientes=clientes, id=id, active1="",active2="", active3="active", active4="")

@app.route("/os")
def os():
    os = getData("key","*", "Cadastro_Os","limit","Numero_os") 
    os_val = getData("val","*", "Cadastro_Os", "limit", "Numero_os")
    os_len = len(os) 
    val_len = len(os_val)
    return render_template("os.html", os=os, os_val= os_val, os_len=os_len, val_len=val_len, active1="",active2="", active3="", active4="active")     

@app.route("/os/imprimir")
def print1():
    return render_template("imprimir_os.html", title= "Inicio", active1="active",active2="", active3="", active4="active")

@app.route("/os/buscar")
def buscar():
    return render_template("buscar_os.html", title= "Inicio", active1="",active2="", active3="", active4="active")