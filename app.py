from flask import Flask, redirect, render_template, request, send_from_directory, abort, flash, url_for
import pandas as pd
import pyodbc
from CoilArt import Zero, Name, cleanZeroLevel, initmenu, std_cost, avg_cost, UnitID, pur_cost, is_number
from CoilArt import *
import time
import sqlite3
from Nomenclature import Nomenclatures
import json
import re
from datetime import datetime

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

        # PN Validation
        if not re.search("\A\d{3}-\d{4}-\d{3}\Z", PN):
            return render_template("ZeroLevel.html", PN="Invalid_Input!", FileName_ZeroLevel="_")

        # In case extracting has any error, return to ZeroLevel page
        try:
            # for info, check the function below
            df = cleanZeroLevel(PN, AXconn)
        except:
            return render_template("ZeroLevel.html", PN="Error: not BOM or inactive BOM exists", FileName_ZeroLevel="_")
            print("Error: not BOM or inactive BOM exists")
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
    rate = exchange_rate()
    # intialize JSON variable for communication
    fly = {
        "PN": "PN",
        "std_cost": "_",
        "std_cost_date": "",
        "avg_cost": "_",
        "avg_cost_date": "",
        "last_cost": "_",
        "last_cost_date": "",
        "std_unit": "unit",
        "invent_unit": "unit",
        "name": "name",
        "Details": "",
        "rate": rate
    }

    if request.method == "POST":
        if request.form["button"] == "calculate":
            # Get PN
            PN = request.form.get("PN")

            ####Debug####
            print('####################################################')
            print(PN)
            #############

            # PN Validation
            if not re.search("\A\d{3}-\d{4}-\d{3}\Z", PN):
                fly["PN"] = "Invalid_Input!"

            else:  # if PN is valid

                #  get cost from AX
                with AXconn:
                    fly["PN"] = PN
                    # get BOM UNIT "inventory"
                    try:
                        fly["invent_unit"] = UnitID(AXconn, [PN])[0]
                    except:
                        fly["PN"] = "Invalid_PN!"

                    # get last avg cost
                    try:
                        COSTAMOUNTSETTLED, QTYSETTLED, fly["avg_cost_date"] = avg_cost(AXconn, [
                            PN])
                        fly["avg_cost"] = COSTAMOUNTSETTLED / QTYSETTLED
                        fly["avg_cost"] = f'{fly["avg_cost"]: .2f}'
                        fly["avg_cost_date"] = fly["avg_cost_date"].strftime(
                            "%d/%m/%Y")
                    except:
                        print("not pass avg cost query")
                        pass

                    # get last pur. cost
                    try:
                        COSTAMOUNTSETTLED, QTYSETTLED, fly["last_cost_date"] = pur_cost(AXconn, [
                            PN])
                        fly["last_cost"] = COSTAMOUNTSETTLED / QTYSETTLED
                        fly["last_cost"] = f'{fly["last_cost"]: .2f}'
                        fly["last_cost_date"] = fly["last_cost_date"].strftime(
                            "%d/%m/%Y")
                    except:
                        print("not pass last pur cost query")
                        pass

                    # get PN description
                    try:
                        fly["name"] = Name(AXconn, [PN])[0]
                    except:
                        pass

                # std cost
                # In case any error, return to empty TotalLandedCost page
                try:
                    cost, unit, details = std_cost(ACCconn, [PN], rate)
                    print(cost)
                    fly["std_cost"] = f'{cost: .2f}'
                    fly["std_unit"] = unit
                    date_object = datetime.strptime(
                        details["Date"], "%Y-%m-%d %H:%M:%S")
                    fly["std_cost_date"] = date_object.strftime("%d/%m/%Y")
                    fly["Details"] = details
                except:
                    print("not pass std_cost query")
                    pass

                print('####################################################')
                # a = json.dumps([fly])
            return render_template("TotalLandedCost.html", fly=fly)
    elif request.method == "GET":
        return render_template("TotalLandedCost.html", fly=fly)


@app.route("/TotalLandedCostWrite", methods=["GET", "POST"])
def TotalLandedCostWrite():
    if request.method == "POST":
        PN = request.form.get('PN')
        if not re.search("\A\d{3}-\d{4}-\d{3}\Z", PN):
            return "USER INPUT ERROR: Invalid PN"

        Unit = request.form.get('Unit')
        if Unit not in ['KG', 'EA', 'SM', 'MT']:
            return "USER INPUT ERROR: Invalid Unit"

        V_price = request.form.get('V_price')
        if not is_number(V_price):
            return "USER INPUT ERROR: Invalid Vendor Price"

        V_Currency = request.form.get('V_Currency')
        if V_Currency == 'CUR':
            return "USER INPUT ERROR: Invalid Vendor Currency"

        Frieght = request.form.get('Frieght')
        if not Frieght:
            Frieght = 0
            Frieght_Currency = 'EGP'
        elif not is_number(Frieght):
            return "USER INPUT ERROR: Invalid Frieght Price"
        else:
            Frieght_Currency = request.form.get('Frieght_Currency')
            if Frieght_Currency == 'CUR':
                return "USER INPUT ERROR: Invalid Frieght Cost"

        Insurance = request.form.get('Insurance')
        if not Insurance:
            Insurance = 0
            Insurance_Currency = 'EGP'
        elif not is_number(Insurance):
            return "USER INPUT ERROR: Invalid Insurance Cost"
        else:
            Insurance_Currency = request.form.get('Insurance_Currency')
            if Insurance_Currency == 'CUR':
                return "USER INPUT ERROR: Invalid Insurance Currency"

        Bank_Charge_Percentage = request.form.get('Bank_Charge_Percentage')
        if not Bank_Charge_Percentage:
            Bank_Charge_Percentage = 0
        elif not is_number(Bank_Charge_Percentage):
            return "USER INPUT ERROR: Invalid Bank Charge Percentage"
        else:
            Bank_Charge_Percentage = float(Bank_Charge_Percentage) / 100

        Customs_Percentage = float(
            request.form.get('Customs_Percentage')) / 100
        if not Customs_Percentage:
            Customs_Percentage = 0
        elif not is_number(Customs_Percentage):
            return "USER INPUT ERROR: Invalid Customs Percentage"
        else:
            Customs_Percentage = float(Customs_Percentage) / 100

        Clearnace = request.form.get('Clearnace')
        if not Clearnace:
            Clearnace = 0
        elif not is_number(Clearnace):
            return "USER INPUT ERROR: Invalid Clearnace Cost"

        eight_Percent = request.form.get('eight_Percent')
        if not eight_Percent:
            eight_Percent = 0
        elif not is_number(eight_Percent):
            return "USER INPUT ERROR: Invalid 8%"

        Others_Percent = request.form.get('Others_Percent')
        if not Others_Percent:
            Others_Percent = 0
        elif not is_number(Others_Percent):
            return "USER INPUT ERROR: Invalid Others Field"

        Volume = request.form.get('Volume')
        if not Volume:
            Volume = 1
        elif not is_number(Volume):
            return "USER INPUT ERROR: Invalid Volume"

        Date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with ACCconn:
            cursor = ACCconn.cursor()

            cursor.execute("""
                    INSERT OR REPLACE INTO DMCStandard(PN, Unit, V_price, V_Currency, Frieght, Frieght_Currency, Insurance, Insurance_Currency,
                    Bank_Charge_Percentage, Customs_Percentage, Clearnace, eight_Percent, Others_Percent, Volume, Date) 
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
                """, (PN, Unit, V_price, V_Currency, Frieght, Frieght_Currency, Insurance, Insurance_Currency,
                           Bank_Charge_Percentage, Customs_Percentage, Clearnace, eight_Percent, Others_Percent,
                           Volume, Date))
            AXconn.commit()

        return "Successful Write!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
