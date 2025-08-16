from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3
import bcrypt
from functions.global_vars import db_file, db_accounts
from functions.search import database
from functions.authentication import create_account, authenticate
from functions.accounts import delete_account, set_password

app = Flask(__name__)
app.config["TEMPLATE_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

words_db = database(db_file, "SELECT id, eng, dai FROM data")
accounts_db = database(db_accounts, "SELECT id, username, email, role FROM accounts")



@app.route("/")
def index():
    if session.get("role") == "admin":
        return redirect("/admin")
    
    return render_template("index.html", data=words_db.get_all("eng"), name=session.get("username"))


@app.route("/admin")
def admin_panel():
    return render_template("admin.html", data=words_db.get_all("eng"), role=session.get("role"))


@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        word_id = request.form.get('word_id')
        eng = request.form.get('eng')
        dai = request.form.get('dai')

        db = sqlite3.connect(db_file)
        db_cur = db.cursor()

        # print(f'{word_id}: {eng} = {dai}')
        db_cur.execute('UPDATE data SET eng = ?, dai = ? WHERE id = ?', [eng, dai, word_id])
        db.commit()
        db_cur.close()

        return redirect("/admin")


@app.route("/search")
def search():
    q = request.args.get("q")
    mode = request.args.get("m")
    search_html = "search.html"

    if mode == "accounts":
        return render_template(search_html, results=accounts_db.search_query('username',q), mode=mode)

    return render_template(search_html, results=words_db.search_query('eng',q), mode=mode)


@app.route("/accounts")
def accounts():
    return render_template("accounts.html", role=session.get("role"), results=accounts_db.get_all('username'))


@app.route("/login", methods=["GET", "POST"])
def login():
    html_file = "login.html"
    if session.get('username'):
            return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        return_value = authenticate(session=session, user_mail=username, password=password)
        if isinstance(return_value,str):
            return return_value
        
        return "success"

    return render_template(html_file)


@app.route("/register", methods=["GET", "POST"])
def register():
    html_file = "register.html"
    if session.get('username'):
            return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        conpassword = request.form.get("conpassword")

        # Form confirmation
        if not username or not email or not password or not conpassword:
            return "Invalid!"

        elif password != conpassword:
            return "Password and Confirm password are not the same!"
        
        # Creating account
        return_value = create_account(session,username,email,password)
        if isinstance(return_value, str):
            return return_value

        return "success"
    
    return render_template(html_file)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/del_account", methods=["GET", "POST"])
def del_account():
    html_file = "accounts.html"
    if request.method == "POST":
        id = request.form.get("user_id")
        delete_account(id)
        return redirect("/accounts")
    return redirect("/accounts")


@app.route("/set_pass", methods=["GET", "POST"])
def set_pass():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        reset_password(user_id,password)
        return redirect("/accounts")
    return redirect("/accounts")
