import pandas as pd
import pyodbc
from CoilArt import *

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQL-SERVER;'
                      'Database=AutoCool_AX6_Live;'
                      'Trusted_Connection=yes;')

PN = ["143-0600-020"]
# PN = "151-0102-036"

# LinesDF = Item_extract(conn, PN)

# for index, row in LinesDF.iterrows():
#     print(row['PN'])

# print(LinesDF)

ZeroLevel = Zero(conn, PN[0])

df = pd.DataFrame(ZeroLevel, columns=["PN"])
print(df)

# with pd.ExcelWriter('output.xlsx') as writer:
#     df.to_excel(writer, sheet_name='Sheet_name_1')
