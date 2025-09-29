from functions.global_vars import db_accounts, db_file, offset_gap
import sqlite3


class database():
    def __init__(self,db,def_query):
        self.db = db
        self.def_query = def_query

    def execute_query(self, query, param=None):
        with sqlite3.connect(self.db) as conn:
            db_cur = conn.cursor()
            if param is None:
                db_cur.execute(query)
            else:
                db_cur.execute(query, param)

            if query.strip().lower().startswith('select'):
                return db_cur.fetchall()

            conn.commit()
            return db_cur.rowcount

    def search_query(self, search_for, param, normal=True, order_by='ENG', limit_count=0, offset=0):
        print(limit_count)
        print(offset)
        print(type(offset))

        if param == '':
            return self.get_all(search_for, limit_count=limit_count, offset=offset)

        db_cur = sqlite3.connect(self.db).cursor()
        modified_q = self.def_query + " " + f"WHERE {search_for} LIKE ?" + " " + f"ORDER BY {order_by} ASC"
        if normal:
            param = f'{param}%'

        if int(offset) > 0:
            print("OK!")
            modified_q = modified_q + f" LIMIT {limit_count} OFFSET {offset}"
        
        db_cur.execute(modified_q, (param,))
        return db_cur.fetchall()
    
    def get_all(self, order_by, limit_count=0, offset=0):
        db_cur = sqlite3.connect(self.db).cursor()
        order_syntax = f"ORDER BY {order_by} ASC"
        if not self.def_query:
            return "no-data"
        if limit_count == 0:
            limit_count = offset_gap

        modified_q = f'{self.def_query} {order_syntax} LIMIT {limit_count}'
        if offset > 0:
            modified_q = modified_q + f' OFFSET {offset}'

        db_cur.execute(modified_q)
        return db_cur.fetchall()
    
    def word_count(self):
        db_cur = sqlite3.connect(self.db).cursor()
        


# def get_all(order_by, mode='words'):
    # if mode == 'words':
        # db = sqlite3.connect(db_file)
        # db_cur = db.cursor()
        # db_cur.execute(f"SELECT id, eng, dai FROM data ORDER BY {order_by} ASC")
    # elif mode == 'accounts':
        # db = sqlite3.connect(db_accounts)
        # db_cur = db.cursor()
        # db_cur.execute(f"SELECT id, username, email, role FROM accounts ORDER BY {order_by} ASC")
    # return db_cur.fetchall()