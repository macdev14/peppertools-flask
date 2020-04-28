import os
import sqlite3
import requests
import urllib.parse
from cs50 import SQL
from flask import redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

db = SQL("sqlite:///peppertools.db")

def getData(pref1, cond1, table, cond3, column = ""):
    if not pref1 or not cond1 or not table:
        return None
    else:   
        conn = sqlite3.connect("peppertools.db")
        conn2 = sqlite3.connect("peppertools.db")
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        db2 = conn2.cursor()
        cond2 = str(cond1)
        table2 = str(table)
        if cond3 == "limit" and column !="":
            db.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
            db2.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
        else:    
            db.execute('SELECT {} FROM {}'.format(cond2, table2))
            db2.execute('SELECT {} FROM {}'.format(cond2,table2))
        
        if pref1 == "key":
            result = list()
            rows = db.fetchone()
            for row in rows.keys():
                result.append(row)
        else:
            result = db2.fetchall()
            
        return result

def valClientes(id):
    cn = sqlite3.connect("peppertools.db")
    db = cn.cursor()
    db.execute("SELECT * FROM Clientes WHERE ID = ?", id)
    result = db.fetchall()
    return result

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def login_user(user, password):
    rows = db.execute('SELECT * FROM usuarios WHERE  ds_login = ?', user)
    if len(rows) != 1 or password != rows[0]["ds_senha"]:
            return redirect('/login')
    else:
        session["user_id"] = rows[0]["ID"]
        return redirect("/")

def underdev():
    return render_template('manutencao.html',  title= "Inicio", active1="",active2="", active3="", active4="active")