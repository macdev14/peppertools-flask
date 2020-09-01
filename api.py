import requests
import urllib.parse
from flask import jsonify
from cs50 import SQL

db = SQL("sqlite:///peppertools.db")

def getNumber(client = 0):
    try:
        if client != 0:
            row = db.execute("SELECT COUNT(*) AS total FROM Cadastro_OS WHERE id_cliente = ? ", client)
        else:
            row = db.execute("SELECT COUNT(*) AS total FROM Cadastro_OS")
        return jsonify(row[0]['total'])
    except:
        return jsonify('Error')

def getAll(option = 'ALL'):
    try:
        if option == 'ALL': 
            stmt = "SELECT * FROM Cadastro_OS"
        else:
            stmt = "SELECT * FROM Cadastro_OS WHERE Numero_Os = " + str(option)   
        
        row = db.execute(stmt)
        return jsonify(row[0])
    except:
        return jsonify("Nothing found")
