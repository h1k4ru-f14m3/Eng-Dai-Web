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
    db = sqlite3.connect(db_file)
    db_cur = db.cursor()
    q = request.args.get("q")
    mode = request.args.get("m")

    if q == "":    
        db_cur.execute("SELECT id, eng, dai FROM data ORDER BY eng ASC")
        datalist = db_cur.fetchall()
        return render_template("search.html", results=datalist, mode=mode)

    db_cur.execute("SELECT id, eng, dai FROM data WHERE eng LIKE ? ORDER BY eng ASC", [q + "%"])
    datalist = db_cur.fetchall()
    return render_template("search.html", results=datalist, mode=mode)

