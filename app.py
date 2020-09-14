from flask import Flask, redirect, render_template, request, send_from_directory, abort
import pandas as pd
import pyodbc
from CoilArt import Zero, Name
import time

app = Flask(__name__)

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=SQL-SERVER;'
                      'Database=AutoCool_AX6_Live;'
                      'Trusted_Connection=yes;')

FileName_ZeroLevel = "NA"
Path_ZeroLevel = "D:\\redirect\\Desktop\\CoilArt-Web\\static\\ZeroLevel\\"
app.config["ZeroLevel"] = "D:\\redirect\\Desktop\\CoilArt-Web\\static\\ZeroLevel"


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/ZeroLevel", methods=["GET", "POST"])
def ZeroLevel():
    global FileName_ZeroLevel
    if request.method == "GET":
        return render_template("ZeroLevel.html", PN="_")
    else:
        PN = request.form.get("PN")
        # In case extracting has any error, return to ZeroLevel page
        try:
            df = cleanZeroLevel(PN)  # check function below in this file
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


@app.route("/ZeroLevel/download", methods=["GET", "POST"])
def download_ZeroLevel():
    global FileName_ZeroLevel
    try:
        return send_from_directory(app.config["ZeroLevel"], filename=FileName_ZeroLevel, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/ACC")
def ACC():
    return render_template("ACC.html")


def cleanZeroLevel(PN):
    """
    Return clean dataframe of Zero level with descriptions in the following order
    PN, Unit, Qty, Description
    using my functions defined in CoilArt.py
    """
    with conn:
        PNs, Qty, Unit = Zero(conn, PN)
    df = pd.DataFrame({
        "PN": PNs,
        "Qty": Qty,
        "Unit": Unit
    })
    df = df.groupby(['PN', 'Unit']).sum()
    df.reset_index(level=['PN', 'Unit'], inplace=True)
    PNs = list(df.loc[:, 'PN'])
    with conn:
        Description = Name(conn, PNs)
    df['Description'] = Description
    return df
