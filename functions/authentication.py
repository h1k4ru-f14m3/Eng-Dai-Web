import sqlite3
import bcrypt
from functions.global_vars import db_accounts
from functions.search import database
import re

db = database(db_accounts, "SELECT id, username, email, role FROM accounts")


def set_session(session, params, values):
    if not isinstance(params, list) or not isinstance(values, list):
        return 'Params and values must be list.'
    
    for i in range(0,len(params)):
        session[params[i]] = values[i]
    return 0


def is_dupe(check_for,input_value):
    print(bool(db.search_query(check_for,input_value)))
    return bool(db.search_query(check_for,input_value))


def create_account(session, username, email, password):
    if is_dupe('username',username) or is_dupe('email',email):
        print(username)
        return "Username or Email Taken!"
    
    salt = bcrypt.gensalt(rounds=12)
    byte_pass = password.encode("utf-8")
    pass_hash = bcrypt.hashpw(byte_pass, salt)

    db.execute_query(query='INSERT INTO accounts (username, email, password) VALUES (?,?,?)', param=(username,email,pass_hash))
    db_results = db.search_query('username', username)
    print(db_results)

    params = ['username', 'email', 'role']
    values = [db_results[0][1], db_results[0][2], db_results[0][3]]

    return [set_session(session,params,values)]


def authenticate(user_mail, password, session):
    email_regex = '^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$'
    find_for = 'username'
    print(f'From function: {user_mail}')
    
    if re.fullmatch(email_regex,user_mail):
        find_for = 'email'

    if not is_dupe(find_for, user_mail):
        return "Invalid credentials."
    
    db_results = db.execute_query(f'SELECT password, username, email, role FROM accounts WHERE {find_for} = ?', (user_mail,))
    pass_in_db = db_results[0][0]
    print(pass_in_db)
    given_pass = password.encode("utf-8")

    if bcrypt.checkpw(given_pass, pass_in_db):
        params = ['username', 'email', 'role']
        values = [db_results[0][1], db_results[0][2], db_results[0][3]]
        set_session(session,params,values)

        return True
    else:
        return False