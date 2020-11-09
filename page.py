from flask import Flask, redirect,render_template, request, session, flash, jsonify, make_response
from model import *
class page:
    
    def __init__(self, table, content = None, edit=False, select = None,):
        self.table = table
        self.Keys = list(globals()[self.table]._meta.fields.keys())
        self.edit = edit
        self.content = content
        self.select = select
        
    def render(self):
        if self.select:
            self.selectlen= len(self.select)
        else:
            self.selectlen = None
        return render_template("Form.html", content=self.content, clients = self.select, cliLen= self.selectlen, TableCol=self.Keys, TableLen = len(self.Keys), table= self.table , edit=self.edit, active1="",active2="", active3="active", active4="")