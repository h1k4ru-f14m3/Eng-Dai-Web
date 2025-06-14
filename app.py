from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)
app.config["TEMPLATE_AUTO_RELOAD"] = True

@app.route("/")
def index():
    db = sqlite3.connect("data.db")
    db_cur = db.cursor()
    db_cur.execute("SELECT eng, dai FROM data ORDER BY eng ASC")
    datalist = db_cur.fetchall()
    return render_template("index.html", data=datalist)

@app.route("/search")
def search():
    db = sqlite3.connect("data.db")
    db_cur = db.cursor()
    q = request.args.get("q")

    if q == "":    
        db_cur.execute("SELECT eng, dai FROM data ORDER BY eng ASC")
        datalist = db_cur.fetchall()
        return render_template("search.html", results=datalist)

    db_cur.execute("SELECT eng, dai FROM data WHERE eng LIKE ? ORDER BY eng ASC", ["%" + q + "%"])
    datalist = db_cur.fetchall()
    return render_template("search.html", results=datalist)

