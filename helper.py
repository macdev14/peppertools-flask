# -*- coding: utf-8 -*-
import os, sqlite3, requests, datetime, jwt, sys
from py_jwt_validator import PyJwtValidator, PyJwtException
#from cs50 import SQL
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
from flask import flash, redirect, render_template, request, session, escape, Response 
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import mysql.connector as sqlite3
from playhouse.shortcuts import model_to_dict, dict_to_model
from model import *
"""
os.environ['SECRET_KEY'] =  "caf3cc4546725599c99158599d443fc815bd137b73b0b69bc804f3ba483aeaa224c75a2b3fc1f35eccfdfef6cdd01858450435ef6daed0c49bf01fbe1e7b3b79"
os.environ['DB'] =  "mysql://rkpmtiv6bbvm81e5:yz1mq64u3h1sab93@nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ztqqdjf98kpnzn4n"
os.environ['HOST']= "nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
os.environ['USER'] =  "rkpmtiv6bbvm81e5"
os.environ['PASSWORD'] = "yz1mq64u3h1sab93"
os.environ['DATABASE'] = "ztqqdjf98kpnzn4n"



db = SQL(os.environ['DB'])
conn = sqlite3.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )"""
#db = SQL("sqlite:///peppertools34.db")
'''def getData(pref1, cond1, table, limit=False, column = ""):
    if not pref1 or not cond1 or not table:
        return None
    else:   
        #conn2 = sqlite3.connect("mysql://rkpmtiv6bbvm81e5:yz1mq64u3h1sab93@nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ztqqdjf98kpnzn4n")
        db2 = db
        cond2 = str(cond1)
        table2 = str(table)
        if limit == True and column !="":
            Cadastro_OS.select().from_(table).order_by(Cadastro_OS.column.desc())
           # print('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
            db.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
            db2.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
        else:
            res = db.execute('SELECT {} FROM {}'.format(cond2, table2))
            print('SELECT {} FROM {}'.format(cond2, table2))
            #db2.execute('SELECT {} FROM {}'.format(cond2,table2))
            rowsE = res[0]
            result = list()
            for row in rowsE:
                result.append(row)
            #return result
           
        if pref1 == "key":
            rows = db.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
            #col = db.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N{}".format(table) )
            field_names = [i[0] for i in rows]
            result = list()
            #print(field_names)
            result = field_names
        elif pref1 == 'val':
          result = db
            
        return result'''


def auth_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization'):
            try: 
                print(request.headers.get('Authorization'))
                jwt.decode(request.headers.get('Authorization'), os.environ['SECRET_KEY'], algorithms=['HS256'])
                return f(*args, **kwargs)
            except jwt.ExpiredSignature:
                return Response('{"Sessão Expirada!"}', status=401, mimetype='application/json')
        return Response('{"unauthorized"}', status=401, mimetype='application/json')
    return decorated_function


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #try:
        if session.get('token'):
            try:
                #print(session.get('token'))
                jwt.decode(session.get('token'), os.environ['SECRET_KEY'], algorithms=['HS256'])
                return f(*args, **kwargs)
            except jwt.ExpiredSignature:
               
                if session.get('osid'): 
                    osid = session.get('osid')
                    session.clear()
                    session['osid'] = osid
                    flash("Log in Expirado!")
                    return redirect('/login')
                else:
                    session.clear()
                   
                    flash("Log in Expirado!")
                    return redirect('/login')
        
        return redirect("/login")
        
    return decorated_function

def login_user(user, password, jwtoken):
    rows=list(usuarios.select().where(usuarios.ds_login == user).dicts())
    #rows=[model_to_dict(row) for row in rows]
    #rows = db.execute("SELECT * FROM usuarios WHERE ds_login = \'"+ user + "\'")
    #print(rows[0]['ds_senha'])
    #print(rows)
    if not rows:
        flash("Login Inválido")
        return redirect('/login')
    if not check_password_hash(rows[0]['ds_senha'], password) or not rows:
        if rows[0]['ds_senha'] != password:
            flash("Login Inválido")
            return redirect('/login')
        pass
    
    token = jwt.encode({'user': user, 'level': rows[0]["nivel"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, jwtoken)
    session["token"] = token.decode('UTF-8')
    session['_permanent'] = token.decode('UTF-8')
    #print(session.get("osid"))
    if session.get("osid"):
        return redirect("os/form/"+str(session['osid']))
    return redirect('/')
            
def valClientes(id):
    rows = Clientes.select().where(Clientes.ID == id)
    rows = [model_to_dict(row) for row in rows]
    return rows

    

def underdev():
    return render_template('manutencao.html',  title= "Inicio", active1="",active2="", active3="", active4="active")

def insertData(list, table, pref1=""):
    final = "error"
    '''    
    stmt = "INSERT INTO "+table+" ("
    values = " VALUES ("

    for val in list:
        if not list[val] or list[val] == val:
            pass
        else:
            stmt = stmt + str(val) + ","
            if not isinstance(list[val], str):
                values = values + str(list[val]) + ","
            else:
                values = values + "\'" + list[val] +  "\'" + ","
    values = values[:-1]
    stmt = stmt[:-1]
    final = stmt + ")" + values + ")"
    #print(final)'''
    #db.execute(final)
    if pref1 == "n_os":
        find = 'SELECT Id FROM Cadastro_OS WHERE Numero_Os = '+ str(list['Numero_Os'])
        rows = db.execute(find)
        return rows[0]['Id']
    find = 'SELECT ID FROM '+ table +' ORDER BY ID DESC LIMIT 1'
    rows = db.execute(find)
    try:
         return rows[0]['Id']
    except:
         return rows[0]['ID']
    else:
         return rows[0]['id']
   
   
    
def getClient( option='ALL'):
    if option == 'ALL':
        rows = Clientes.select(Clientes.ID, Clientes.nome).join(Cadastro_OS, on=(Cadastro_OS.Id_Cliente == Clientes.ID)).distinct()
        rows = [model_to_dict(row) for row in rows]
        #rows = db.execute('SELECT DISTINCT Clientes.ID, nome FROM Cadastro_OS, Clientes WHERE Cadastro_OS.id_cliente = Clientes.ID')
    else:
        rows = Clientes.select(Clientes.ID, Clientes.nome).join(Cadastro_OS, on=(Cadastro_OS.Id_Cliente == Clientes.ID, Cadastro_OS.Id == option)).distinct()
        rows = [model_to_dict(row) for row in rows]
        #rows = db.execute('SELECT DISTINCT nome FROM Cadastro_OS, Clientes WHERE Cadastro_OS.id_cliente = Clientes.ID AND Cadastro_OS.Id = ?', option) 
        rows = rows[0]
    return rows

def getOs(option = 'ALL'):
    if option == 'ALL':
        rows = int(Cadastro_OS.select(fn.MAX(Cadastro_OS.Numero_Os)).scalar())+1
       # rows = int(rows[0]['num_os']) + 1
    else:
        stmt = 'SELECT * FROM Cadastro_OS WHERE Id = '+ str(option)
        rows = os = Cadastro_OS.select().where(Cadastro_OS == osid)
    return rows

def updateData(list, table, col, Id):
  #  print(list)
    stmt = "UPDATE " + table + " SET "
    values = ""
    for item in list:
        if not list[item] or list[item] == item or item == 'id':
            pass
        else:
            if not isinstance(list[item], str):
                values = values + item + "=" + str(list[item]) + ","
            elif item == 'Id' or item == 'ID':
                pass
            else:
                values = values + item + "= \'" + list[item] +  "\'" + ","
       
    values = values[:-1]
    values = values + " WHERE "+col+" = "+ str(Id)
    final = stmt + values
    #print(final)
    db.execute(final)
    return 
    
    

def deleteData(table,col,Id):
    try:
        db.execute('DELETE FROM ' + table + ' WHERE ' + col + ' = ' + str(Id))
        return redirect('/os')
    except:
        return redirect('/os/form/' + str(Id))
    
def checkDate(str1):
    
    str2 = str1
    try:
        print (len(str1))
        if len(str1) != 10:
            str2 = ''
            str2 = '0' + str1
            str2 = datetime.datetime.strptime(str2, '%m/%d/%y, %H:%M:%S %p').strftime('%d/%m/%Y')  
        else:
            str2 = ''
            str2 = datetime.datetime.strptime(str1, '%d/%m/%Y').strftime('%d/%m/%Y')
    except:
        pass
    
         
    return str2

def render_list(table):
    print(table)
    try:
        tblist = str_to_class(table).select().distinct()
        keys = list(str_to_class(table)._meta.fields.keys())
    except:
        try:
            tblist = str_to_class(table.capitalize()).select().distinct()
            keys = list(str_to_class(table.capitalize())._meta.fields.keys())
        except:
            flash('Erro ao encontrar!')
            return redirect('/')    
    
    
    tblist = [model_to_dict(row) for row in tblist]
    
    if 'Id_Cliente' in keys or 'id_cliente' in keys:
        try:
            i = keys.index('Id_Cliente')
        except:
            i = keys.index('id_cliente')
        keys[i] = 'Nome'
        for j in tblist:
            try:
                nome = list(Clientes.select(Clientes.nome).where(Clientes.ID == j.Id_Cliente).dicts())
                print(nome)
                #nome = nome[0]['nome']
                j.Id_Cliente = nome
                
            except:
                pass
          #  try:
            print('Loop:')
            print(j)
            nome = list(Clientes.select(Clientes.nome).where(Clientes.ID == j['id_cliente']).dicts())
            if nome:
                nome = nome[0]['nome']
                j['Nome'] = nome
            else: 
                j['Nome'] = 'Inexistente'
            
          #  except:
          #      pass
    '''
    try:
        tblist = str_to_class(table).select()
        tblist = [model_to_dict(row) for row in tblist]
        keys = str_to_class(table)._meta.fields.keys()
    except Exception as e:
        print(e)
        flash('Erro ao carregar item(s)')
        return redirect('/')'''
    
    if 'cod_fornecedor' in keys:
        i = keys.index('cod_fornecedor')
        keys[i] = 'Fornecedor'
        for j in tblist:
            nome = list(Fornecedores.select(Fornecedores.nome).where(Fornecedores.ID == j['cod_fornecedor']))
            if nome:
                nome = nome[0]['nome']
                j['Fornecedor'] = nome
            else: 
                j['Fornecedor'] = 'Inexistente'
    
    if 'data_pagamento' in keys:
        for j in tblist:
            if j['data_pagamento']:
                pass
            else:
                j['data_pagamento'] = 'Não foi pago'
    print(tblist)
    return render_template('list.html', keys=keys, content=tblist, table=table)

   
            
    


def logoutCommit():
    session.clear()
    return redirect('/login')

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

def registerprocess(id_proc, id_os, inicio=None, fim=None, ):
    if inicio and not fim:
       Historico_os.create(inicio=inicio, id_proc=id_proc, id_os=id_os)
       return True
    if fim and not inicio:
       Historico_os.create(fim=fim, id_proc=id_proc, id_os=id_os)
       return True
    if not inicio and not fim:
       Historico_os.create(id_proc=id_proc, id_os=id_os)
       return True
    else:
       Historico_os.create(inicio=inicio, fim=fim, id_proc=id_proc, id_os=id_os)
       return True