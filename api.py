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