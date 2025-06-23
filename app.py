from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)
app.config["TEMPLATE_AUTO_RELOAD"] = True

db_file = "data.db"

def get_all(order_by):
    db = sqlite3.connect("data.db")
    db_cur = db.cursor()
    
    db_cur.execute(f"SELECT id, eng, dai FROM data ORDER BY {order_by} ASC")
    return db_cur.fetchall()

@app.route("/")
def index():
    return render_template("index.html", data=get_all("eng"))

@app.route("/admin")
def admin_panel():
    return render_template("admin.html", data=get_all("eng"))

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        for i in get_all('eng'):
            print(f"{i[0]} = {i[1]}")
        return redirect("/")
    
@app.route("/dosomething")
def dosomething():
    return render_template("admin.html", data=get_all('eng'))

@app.route("/search")
def search():
    db = sqlite3.connect(db_file)
    db_cur = db.cursor()
    q = request.args.get("q")

    if q == "":    
        db_cur.execute("SELECT id, eng, dai FROM data ORDER BY eng ASC")
        datalist = db_cur.fetchall()
        return render_template("search.html", results=datalist)

    db_cur.execute("SELECT id, eng, dai FROM data WHERE eng LIKE ? ORDER BY eng ASC", [q + "%"])
    datalist = db_cur.fetchall()
    return render_template("search.html", results=datalist)

