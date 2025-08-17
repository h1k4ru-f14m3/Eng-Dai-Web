from functions.accounts import database
from functions.global_vars import reset_session, json_file, db_accounts
import json

db = database(db_accounts, "SELECT id, role FROM accounts")

def init_json():
    global reset_session
    with open(json_file) as f:
        reset_session = json.load(f)
        # reset_session.append(reset_session[(len(reset_session) - 1)] + 1)
        # print(reset_session)


def save_json():
    print(reset_session)
    with open(json_file, 'w') as f:
        json.dump(reset_session, f, indent=4)


def check_role(id, session, session_type):
    global reset_session
    if id in reset_session:
        role = db.execute_query("SELECT role FROM accounts WHERE id = ?", (id,))
        session[session_type] = role[0][0]
        reset_session.remove(id)
        print(session[session_type])


def set_role(id, role):
    db.execute_query("UPDATE accounts SET role = ? WHERE id = ?", (role, id))
    global reset_session
    if id not in reset_session:
        reset_session.append(int(id))