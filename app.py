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
        return render_template("ZeroLevel.html")
    else:
        PN = request.form.get("PN")
        LinesDF = Item_extract(conn, PN)
        row_data = list(LinesDF.values.tolist())
        return render_template("ZeroLevel.html", PN=PN, row_data=row_data)
