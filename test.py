# import pandas as pd
import pyodbc
from CoilArt import *
import sqlite3
# import sqlite3

AXconn = pyodbc.connect('Driver={SQL Server};'
                        'Server=SQL-SERVER;'
                        'Database=AutoCool_AX6_Live;'
                        'Trusted_Connection=yes;')

Path_SQLite3Database = "D:\\redirect\\Desktop\\CoilArt-Web\\static\\database\\"
ACCconn = sqlite3.connect(Path_SQLite3Database +
                          "ACC.db", check_same_thread=False)

print(std_cost(ACCconn, ["148-0102-001"]))

# Path_SQLite3Database = "D:\\redirect\\Desktop\\CoilArt-Web\\static\\database\\"
# ACCconn = sqlite3.connect(Path_SQLite3Database +
#                           "ACC.db", check_same_thread=False)

# with ACCconn:
#     PN = ["148-0102-009"]
#     cost, unit = DMCStandard(ACCconn, PN)
#     print(cost)

# with conn:
# PN = ["143-0600-020"]
# # PN = "151-0102-036"

# # LinesDF = Item_extract(conn, PN)

# # for index, row in LinesDF.iterrows():
# #     print(row['PN'])

# # print(LinesDF)

# PN, Qty, Unit = Zero(conn, PN)
# # Description = Name(conn, PN)

# df = pd.DataFrame({
#     "PN": PN,
#     "Qty": Qty,
#     "Unit": Unit
# })

# cdf = df.groupby(by=["PN", "Unit"]).sum()
# print(cdf)

# # cdf['test'] = cdf.index
# cdf.reset_index(level=['PN', 'Unit'], inplace=True)
# print(cdf)
# print(list(cdf.loc[:, 'PN']))

# # with pd.ExcelWriter('output.xlsx') as writer:
# #     cdf.to_excel(writer, sheet_name='Sheet_name_1')

####################################################################

# import requests

# # Where USD is the base currency you want to use
# url = 'https://v6.exchangerate-api.com/v6/6c4a907e81f1a523b321dae3/latest/USD'

# # Making our request
# response = requests.get(url)
# data = response.json()

# # Your JSON object
# print(data)

###################################################################

# from forex_python.converter import CurrencyRates
# c = CurrencyRates()
# c.get_rates('USD')   # you can directly call get_rates('USD')

##################################################################

# # Python program to get the real-time
# # currency exchange rate

# # Function to get real time currency exchange
# def RealTimeCurrencyExchangeRate(from_currency, to_currency, api_key):

#     # importing required libraries
#     import requests
#     import json

#     # base_url variable store base url
#     base_url = r"https://www.alphavantage.co/query?function = CURRENCY_EXCHANGE_RATE"

#     # main_url variable store complete url
#     main_url = base_url + "&from_currency =" + from_currency + \
#         "&to_currency =" + to_currency + "&apikey =" + api_key

#     # get method of requests module
#     # return response object
#     req_ob = requests.get(main_url)

#     # json method return json format
#     # data into python dictionary data type.

#     # result contains list of nested dictionaries
#     result = req_ob.json()

#     print(" Result before parsing the json data :\n", result)

#     print("\n After parsing : \n Realtime Currency Exchange Rate for",
#           result["Realtime Currency Exchange Rate"]
#           ["2. From_Currency Name"], "TO",
#           result["Realtime Currency Exchange Rate"]
#           ["4. To_Currency Name"], "is",
#           result["Realtime Currency Exchange Rate"]
#           ['5. Exchange Rate'], to_currency)


# # Driver code
# if __name__ == "__main__":

#     # currency code
#     from_currency = "USD"
#     to_currency = "INR"

#     # enter your api key here
#     # api_key = "HU77CPZ8TBVIKQ9G"
#     api_key = "CX1NMNPQUV5NJ4Q5"

#     # function calling
#     RealTimeCurrencyExchangeRate(from_currency, to_currency, api_key)
##################################################################################
# from PyCurrency import codes
# codes()
