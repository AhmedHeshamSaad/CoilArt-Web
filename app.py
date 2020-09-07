from flask import Flask, redirect, render_template, request
import pandas as pd
import pyodbc
from CoilArt import *

app = Flask(__name__)

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQL-SERVER;'
                      'Database=AutoCool_AX6_Live;'
                      'Trusted_Connection=yes;')


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/ZeroLevel", methods=["GET", "POST"])
def ZeroLevel():
    if request.method == "GET":
        return render_template("ZeroLevel.html", PN="_")
    else:
        PN = request.form.get("PN")
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
        row_data = list(df.values.tolist())
        return render_template("ZeroLevel.html", PN=PN, row_data=row_data)
