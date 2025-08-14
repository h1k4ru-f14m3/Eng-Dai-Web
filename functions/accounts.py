from functions.search import database
from functions.global_vars import db_accounts
import bcrypt


db = database(db_accounts,'SELECT id, username, email, role FROM accounts')


def delete_account(id):
    db.execute_query("DELETE FROM accounts WHERE id = ?", (id,))
    return "Success!"


# TODO: make it set password, having a password as a parameter
def set_password(id, password):
    salt = bcrypt.gensalt(rounds=12)
    default_pass = password.encode("utf-8")
    pass_hash = bcrypt.hashpw(default_pass, salt)

    db.execute_query("UPDATE accounts SET password = ? WHERE id = ?", (pass_hash,id))