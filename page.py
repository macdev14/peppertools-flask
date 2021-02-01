from flask import Flask, redirect,render_template, request, session, flash, jsonify, make_response
from model import *
class page:
    '''
    arg: 
    table, content, edit, select, select2
    '''
    def __init__(self, table, content = None, edit=False, select = None, select2 = None):
        self.col = []
        self.table = table
        self.Keys = list(globals()[self.table]._meta.fields.keys())
        self.edit = edit
        self.content = content
        self.select = select
        self.select2 = select2
        for i in range(len(self.Keys)):
            if 'cod_' in self.Keys[i] or 'id_' in self.Keys[i] or 'Id_' in self.Keys:
                self.col.append(self.Keys[i])
    def render(self): 
        if self.select:
            self.selectlen= len(self.select)
        else:
            self.selectlen = None 
        if len(self.col) == 2:
            return render_template("Form.html", content=self.content, clients = self.select, cliLen= self.selectlen, cliCol=self.col[0] , selection2=self.select2, sel2Col = self.col[1], sel2Len=len(self.select2), TableCol=self.Keys, TableLen = len(self.Keys), table= self.table.lower() , edit=self.edit, active1="",active2="", active3="active", active4="")
        elif len(self.col) == 1:
            return render_template("Form.html", content=self.content, clients = self.select, cliCol=self.col[0], cliLen= self.selectlen, TableCol=self.Keys, TableLen = len(self.Keys), table= self.table.lower() , edit=self.edit, active1="",active2="", active3="active", active4="")
        else:
            return render_template("Form.html", content=self.content, TableCol=self.Keys, TableLen = len(self.Keys), table= self.table.lower() , edit=self.edit, active1="",active2="", active3="active", active4="")