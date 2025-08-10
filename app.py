from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3
import bcrypt

app = Flask(__name__)
app.config["TEMPLATE_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_file = "data.db"
db_accounts = "accounts.db"

def get_all(order_by):
    db = sqlite3.connect("data.db")
    db_cur = db.cursor()
    
    db_cur.execute(f"SELECT id, eng, dai FROM data ORDER BY {order_by} ASC")
    return db_cur.fetchall()

@app.route("/")
def index():
    if session.get("role") == "admin":
        return redirect("/admin")
    return render_template("index.html", data=get_all("eng"), name=session.get("username"))

@app.route("/admin")
def admin_panel():
    return render_template("admin.html", data=get_all("eng"), role=session.get("role"))

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        word_id = request.form.get('word_id')
        eng = request.form.get('eng')
        dai = request.form.get('dai')

        db = sqlite3.connect(db_file)
        db_cur = db.cursor()

        print(f'{word_id}: {eng} = {dai}')
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
        db = sqlite3.connect(db_accounts)
        db_cur = db.cursor()

        if q == "":
            db_cur.execute("SELECT id, username, email, role FROM accounts ORDER BY id ASC")
            return render_template(search_html, results=db_cur.fetchall())
        
        db_cur.execute("SELECT id, username, email, role FROM accounts WHERE username LIKE ? OR email LIKE ? ORDER BY id ASC", (q + "%", q + "%"))
        return render_template(search_html, results=db_cur.fetchall())

    db = sqlite3.connect(db_file)
    db_cur = db.cursor()

    if q == "":    
        db_cur.execute("SELECT id, eng, dai FROM data ORDER BY eng ASC")
        datalist = db_cur.fetchall()
        return render_template(search_html, results=datalist, mode=mode)

    db_cur.execute("SELECT id, eng, dai FROM data WHERE eng LIKE ? ORDER BY eng ASC", [q + "%"])
    datalist = db_cur.fetchall()
    return render_template(search_html, results=datalist, mode=mode)


@app.route("/accounts")
def accounts():
    db = sqlite3.connect(db_accounts)
    db_cur = db.cursor()

    db_cur.execute("SELECT id, username, email, role FROM accounts ORDER BY id ASC")    

    return render_template("accounts.html", role=session.get("role"), results=db_cur.fetchall())


@app.route("/login", methods=["GET", "POST"])
def login():
    html_file = "login.html"
    if request.method == "POST":
        db = sqlite3.connect(db_accounts)
        db_cur = db.cursor()
        
        db_cur.execute("SELECT * FROM accounts WHERE username = ?", (request.form.get("username"),))
        acc_data = db_cur.fetchone()
        if not acc_data:
            db_cur.execute("SELECT * FROM accounts WHERE email = ?", (request.form.get("username"),))
            acc_data = db_cur.fetchone()
        
        if not acc_data:
            return render_template(html_file, message="Username or Email not found!")
        
        pass_hash = acc_data[3]
        given_pass = request.form.get("password").encode("utf-8")
        
        if bcrypt.checkpw(given_pass, pass_hash):
            session["username"] = acc_data[1]
            session["role"] = acc_data[4]
            session["email"] = acc_data[2]

            db.close()
            return redirect("/")
        db.close()
        return render_template(html_file, message="Invalid password!")

    return render_template(html_file)

@app.route("/register", methods=["GET", "POST"])
def register():
    html_file = "register.html"

    if request.method == "POST":
        db = sqlite3.connect(db_accounts)
        db_cur = db.cursor()

        db_cur.execute("SELECT * FROM accounts WHERE username = ?", (request.form.get("username"),))
        user_taken_test = db_cur.fetchone()

        db_cur.execute("SELECT * FROM accounts WHERE email = ?", (request.form.get("email"),))
        emaiL_taken_test = db_cur.fetchone()

        if not request.form.get("username") or not request.form.get("email") or not request.form.get("password") or not request.form.get("conpassword"):
            return render_template(html_file, message="Invalid!")
        
        elif user_taken_test:
            return render_template(html_file, message="Username taken!")
        
        elif emaiL_taken_test:
            return render_template(html_file, message="Email already taken!")

        elif request.form.get("password") != request.form.get("conpassword"):
            return render_template(html_file, message="Password and Confirm password are not the same!")
        
        salt = bcrypt.gensalt(rounds=12)
        byte_pass = request.form.get("password").encode("utf-8")
        pass_hash = bcrypt.hashpw(byte_pass, salt)
        
        db_cur.execute("INSERT INTO accounts (username, email, password) VALUES (?,?,?)", (request.form.get("username"), request.form.get("email"), pass_hash))
        session["username"] = request.form.get("username")
        session["email"] = request.form.get("email")
        db.commit()
        db_cur.close()

        return redirect("/")
    return render_template(html_file)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")