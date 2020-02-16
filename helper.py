import sqlite3



def getData(pref1, cond1, table, cond3, column):
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

