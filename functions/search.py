from functions.global_vars import db_accounts, db_file
import sqlite3


class database():
    def __init__(self,db,def_query):
        self.db = db
        self.def_query = def_query

    def execute_query(self, search_for, param):
        if param == '':
            return self.get_all(search_for)

        db_cur = sqlite3.connect(self.db).cursor()
        modified_q = self.def_query + " " + f"WHERE {search_for} LIKE ?"
        db_cur.execute(modified_q, (f'{param}%',))
        return db_cur.fetchall()
    
    def get_all(self, order_by):
        db_cur = sqlite3.connect(self.db).cursor()
        order_syntax = f"ORDER BY {order_by} ASC"
        if not self.def_query:
            return "no-data"
        db_cur.execute(f'{self.def_query} {order_syntax}')
        return db_cur.fetchall()

def get_all(order_by, mode='words'):
    if mode == 'words':
        db = sqlite3.connect(db_file)
        db_cur = db.cursor()
        db_cur.execute(f"SELECT id, eng, dai FROM data ORDER BY {order_by} ASC")
    elif mode == 'accounts':
        db = sqlite3.connect(db_accounts)
        db_cur = db.cursor()
        db_cur.execute(f"SELECT id, username, email, role FROM accounts ORDER BY {order_by} ASC")
    return db_cur.fetchall()