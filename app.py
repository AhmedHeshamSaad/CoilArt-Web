from flask import Flask, redirect, render_template, request, send_from_directory, abort, flash, url_for
import pandas as pd
import pyodbc
from CoilArt import Zero, Name, cleanZeroLevel, initmenu, std_cost, avg_cost, UnitID, pur_cost
import time
import sqlite3
from Nomenclature import Nomenclatures
import json
import re

app = Flask(__name__)
app.secret_key = 'Hesham'

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
    # global FileName_ZeroLevel
    if request.method == "POST":
        PN = request.form.get("PN")
        # In case extracting has any error, return to ZeroLevel page
        try:
            # for info, check the function below
            df = cleanZeroLevel(PN, AXconn)
        except:
            return render_template("ZeroLevel.html", PN="_", FileName_ZeroLevel="_")
            print("# Extraction Failed")
            # alert("Unvalid input")

        # export to excel file if user gonna download it
        if request.form.getlist("checkbox"):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            FileName_ZeroLevel = PN + " ZeroLevel " + timestr + ".xlsx"
            with pd.ExcelWriter(Path_ZeroLevel + FileName_ZeroLevel) as writer:  # pylint: disable=abstract-class-instantiated
                df.to_excel(writer, sheet_name='Zerolevel')

        # return date to the template
        row_data = list(df.values.tolist())
        return render_template("ZeroLevel.html", PN=PN, FileName_ZeroLevel=FileName_ZeroLevel, row_data=row_data)

    return render_template("ZeroLevel.html", PN="_", FileName_ZeroLevel="_")


@app.route("/ZeroLevel/download/<FileName_ZeroLevel>")
def download_ZeroLevel(FileName_ZeroLevel):
    # global FileName_ZeroLevel
    try:
        return send_from_directory(app.config["ZeroLevel"], filename=FileName_ZeroLevel, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/ACC")
def ACC():
    menu = initmenu(ACCconn)
    return render_template("ACC.html", menu=menu)


# @app.route("/CodeNomenclature")
# def CodeNomenclature():
#     return render_template("CodeNomenclature.html")


@app.route("/Nomenclature")
def Nomenclature():
    return render_template("Nomenclature.html", Nomenclatures=Nomenclatures)


@app.route("/TotalLandedCost", methods=["GET", "POST"])
def TotalLandedCost():
    fly = {
        "PN": "PN",
        "std_cost": "_",
        "avg_cost": "_",
        "std_unit": "unit",
        "avg_unit": "unit",
        "name": "name",
        "Details": ""
    }
    if request.method == "POST":
        if request.form["button"] == "calculate":
            PN = request.form.get("PN")
            print('####################################################')
            print(PN)
            fly["PN"] = PN

            #  cost from AX
            with AXconn:
                fly["avg_unit"] = UnitID(AXconn, [PN])[0]
                try:
                    fly["avg_cost"] = f'{avg_cost(AXconn, [PN])[0]: .2f}'
                except:
                    try:
                        fly["avg_cost"] = f'{pur_cost(AXconn, [PN])[0]: .2f}'
                    except:
                        pass
                try:
                    fly["name"] = Name(AXconn, [PN])[0]
                except:
                    pass

            # In case any error, return to empty TotalLandedCost page
            try:
                cost, unit, details = std_cost(ACCconn, [PN])
                print(cost)
                fly["std_cost"] = f'{cost: .2f}'
                fly["std_unit"] = unit
                fly["Details"] = details
            except:
                # alert("Unvalid input")
                # return render_template("TotalLandedCost.html", fly=fly)
                print("not pass")
                pass

            print('####################################################')
            # a = json.dumps([fly])
            return render_template("TotalLandedCost.html", fly=fly)
    elif request.method == "GET":
        return render_template("TotalLandedCost.html", fly=fly)


@app.route("/TotalLandedCostWrite", methods=["GET", "POST"])
def TotalLandedCostWrite():
    if request.method == "POST":
        # if re.search("\A\d{3}-\d{4}-\d{3}\Z", txt) else return ""
        PN = request.form.get('PN')
        Unit = request.form.get('Unit')
        V_price = request.form.get('V_price')
        V_Currency = request.form.get('V_Currency')
        Frieght = request.form.get('Frieght')
        Frieght_Currency = request.form.get('Frieght_Currency')
        Insurance = request.form.get('Insurance')
        Insurance_Currency = request.form.get('Insurance_Currency')
        Bank_Charge_Percentage = float(
            request.form.get('Bank_Charge_Percentage')) / 100
        Customs_Percentage = float(
            request.form.get('Customs_Percentage')) / 100
        Clearnace = request.form.get('Clearnace')
        eight_Percent = request.form.get('eight_Percent')
        Others_Percent = request.form.get('Others_Percent')
        Volume = request.form.get('Volume')

        with ACCconn:
            cursor = ACCconn.cursor()

            cursor.execute("""
                    INSERT OR REPLACE INTO DMCStandard(PN, Unit, V_price, V_Currency, Frieght, Frieght_Currency, Insurance, Insurance_Currency,
                    Bank_Charge_Percentage, Customs_Percentage, Clearnace, eight_Percent, Others_Percent, Volume) 
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);
                """, (PN, Unit, V_price, V_Currency, Frieght, Frieght_Currency, Insurance, Insurance_Currency,
                           Bank_Charge_Percentage, Customs_Percentage, Clearnace, eight_Percent, Others_Percent,
                           Volume))
            AXconn.commit()

        return "Successful Write!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
