import pandas as pd
import pyodbc
from CoilArt import *

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQL-SERVER;'
                      'Database=AutoCool_AX6_Live;'
                      'Trusted_Connection=yes;')

with conn:
    PN = ["143-0600-020"]
    # PN = "151-0102-036"

    # LinesDF = Item_extract(conn, PN)

    # for index, row in LinesDF.iterrows():
    #     print(row['PN'])

    # print(LinesDF)

    PN, Qty, Unit = Zero(conn, PN)
    # Description = Name(conn, PN)

    df = pd.DataFrame({
        "PN": PN,
        "Qty": Qty,
        "Unit": Unit
    })

    cdf = df.groupby(by=["PN", "Unit"]).sum()
    print(cdf)

    # cdf['test'] = cdf.index
    cdf.reset_index(level=['PN', 'Unit'], inplace=True)
    print(cdf)
    print(list(cdf.loc[:, 'PN']))

    # with pd.ExcelWriter('output.xlsx') as writer:
    #     cdf.to_excel(writer, sheet_name='Sheet_name_1')
