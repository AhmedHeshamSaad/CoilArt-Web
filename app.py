from flask import Flask, redirect, render_template, request, send_from_directory, abort
import pandas as pd
import pyodbc
from CoilArt import Zero, Name, cleanZeroLevel, initmenu
import time
import sqlite3

app = Flask(__name__)

AXconn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=SQL-SERVER;'
                        'Database=AutoCool_AX6_Live;'
                        'Trusted_Connection=yes;')

Path_SQLite3Database = "D:\\redirect\\Desktop\\CoilArt-Web\\static\\database\\"
ACCconn = sqlite3.connect(Path_SQLite3Database +
                          "ACC.db", check_same_thread=False)

FileName_ZeroLevel = "NA"
Path_ZeroLevel = "D:\\redirect\\Desktop\\CoilArt-Web\\static\\ZeroLevel\\"
app.config["ZeroLevel"] = "D:\\redirect\\Desktop\\CoilArt-Web\\static\\ZeroLevel"


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/ZeroLevel", methods=["GET", "POST"])
def ZeroLevel():
    global FileName_ZeroLevel
    if request.method == "POST":
        PN = request.form.get("PN")
        # In case extracting has any error, return to ZeroLevel page
        try:
            # check function below in this file
            df = cleanZeroLevel(PN, AXconn)
        except:
            return render_template("ZeroLevel.html", PN="_")

        # export to excel file if user gonna download it
        if request.form.getlist("checkbox"):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            FileName_ZeroLevel = PN + " ZeroLevel " + timestr + ".xlsx"
            with pd.ExcelWriter(Path_ZeroLevel + FileName_ZeroLevel) as writer:
                df.to_excel(writer, sheet_name='Zerolevel')

        # return date to the template
        row_data = list(df.values.tolist())
        return render_template("ZeroLevel.html", PN=PN, row_data=row_data)

    return render_template("ZeroLevel.html", PN="_")


@app.route("/ZeroLevel/download", methods=["GET", "POST"])
def download_ZeroLevel():
    global FileName_ZeroLevel
    try:
        return send_from_directory(app.config["ZeroLevel"], filename=FileName_ZeroLevel, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/ACC")
def ACC():
    menu = initmenu(ACCconn)
    return render_template("ACC.html", menu=menu)


@app.route("/CodeNomenclature")
def CodeNomenclature():
    return render_template("CodeNomenclature.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
