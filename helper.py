import os, sqlite3, requests, urllib.parse, datetime, jwt
from py_jwt_validator import PyJwtValidator, PyJwtException
from cs50 import SQL
from flask import flash, redirect, render_template, request, session, escape, Response 
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import mysql.connector as sqlite3

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
        )
def getData(pref1, cond1, table, limit=False, column = ""):
    if not pref1 or not cond1 or not table:
        return None
    else:   
        #conn2 = sqlite3.connect("mysql://rkpmtiv6bbvm81e5:yz1mq64u3h1sab93@nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ztqqdjf98kpnzn4n")
        db = conn.cursor(buffered=True)
        db2 = db
        cond2 = str(cond1)
        table2 = str(table)
        if limit == True and column !="":
           # print('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
            db.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
            db2.execute('SELECT {} FROM {} ORDER BY {} DESC'.format(cond2,table2, column))
        else:
            db.execute('SELECT {} FROM {}'.format(cond2, table2))
            print('SELECT {} FROM {}'.format(cond2, table2))
            #db2.execute('SELECT {} FROM {}'.format(cond2,table2))
            rowsE = db.fetchone()
            result = list()
            for row in rowsE:
                result.append(row)
            #return result
           
        if pref1 == "key":
            #num_fields = len(db.description)
            field_names = [i[0] for i in db.description]
            result = list()
            #print(field_names)
            result = field_names
        elif pref1 == 'val':
          result = db2.fetchall()
            
        return result

def valClientes(id):
    cn = sqlite3.connect("mysql://rkpmtiv6bbvm81e5:yz1mq64u3h1sab93@nwhazdrp7hdpd4a4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ztqqdjf98kpnzn4n")
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
        #try:
        if session.get('token'):
            try:
                #print(session.get('token'))
                jwt.decode(session.get('token'), os.environ['SECRET_KEY'], algorithms=['HS256'])
                return f(*args, **kwargs)
            except jwt.ExpiredSignature:
                conn.commit()
                if session.get('osid'): 
                    osid = session.get('osid')
                    session.clear()
                    session['osid'] = osid
                    flash("Log in Expirado!")
                    return redirect('/login')
                else:
                    session.clear()
                    conn.close()
                    flash("Log in Expirado!")
                    return redirect('/login')
        return redirect("/login")
        
    return decorated_function

def login_user(user, password, jwtoken):
    rows = db.execute("SELECT * FROM usuarios WHERE ds_login = \'"+ user + "\'")
    if len(rows) != 1 or not check_password_hash(rows[0]["ds_senha"], password):
            flash("Login Inválido")
            return redirect('/login')
    else:
         token = jwt.encode({'user': user, 'level': rows[0]["nivel"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, jwtoken)
         session["token"] = token.decode('UTF-8')
         session['_permanent'] = token.decode('UTF-8')
         if session.get("osid"):
            if session.get("_permanent") or request.headers.get('authorization'):
                return redirect("os/form/"+str(session['osid']))
            else:
                return redirect('/login')
         return redirect('/')
            

def underdev():
    return render_template('manutencao.html',  title= "Inicio", active1="",active2="", active3="", active4="active")

def insertData(list, table, pref1=""):
    final = "error"
    
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
    #print(final)
    db.execute(final)
    if pref1 == "n_os":
        find = 'SELECT Id FROM Cadastro_OS WHERE Numero_Os = '+ str(list['Numero_Os'])
        rows = db.execute(find)
        return rows[0]['Id']
    find = 'SELECT ID FROM '+ table +' ORDER BY ID DESC LIMIT 1'
    rows = db.execute(find)
    return rows[0]['ID']
   
    
def getClient( option='ALL'):
    if option == 'ALL':
        rows = db.execute('SELECT DISTINCT Clientes.ID, nome FROM Cadastro_OS, Clientes WHERE Cadastro_OS.id_cliente = Clientes.ID')
    else:
        rows = db.execute('SELECT DISTINCT nome FROM Cadastro_OS, Clientes WHERE Cadastro_OS.id_cliente = Clientes.ID AND Cadastro_OS.Id = ?', option) 
        rows = rows[0]
    return rows

def getOs(option = 'ALL'):
    if option == 'ALL':
        rows = db.execute('SELECT MAX(Numero_Os) AS num_os FROM Cadastro_OS')
        rows = int(rows[0]['num_os']) + 1
    else:
        stmt = 'SELECT * FROM Cadastro_OS WHERE Id = '+ str(option)
        rows = db.execute(stmt)   
    return rows

def updateData(list, table, col, Id):
    db = conn.cursor()
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

def auth_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('authorization'):
            request.headers.get('authorization') 
            return f(*args, **kwargs)
        else:
             return Response('{"unauthorized"}', status=401, mimetype='application/json')
    return decorated_function

def logoutCommit():
    conn.commit()
    conn.close()
    session.clear()
    return redirect('/login')