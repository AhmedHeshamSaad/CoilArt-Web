import pandas as pd
import pyodbc
import itertools


class Item:
    def __init__(self, PN, Qty, UNITID, Parent, BOM=None):
        self.PN = PN
        self.UNITID = UNITID
        self.parent = Parent
        self.BOM = BOM


def Name(conn, PNList):
    Names = []
    for PN in PNList:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT NAME
            FROM INVENTITEMPRICECOMPAREITEMVIEW
            WHERE ITEMID = ?
            """, PN)
        Names.append(cursor.fetchall()[0][0])

    return Names


def UnitID(AXconn, PN):
    unit = []
    with AXconn:
        cursor = AXconn.cursor()
        cursor.execute("""
            SELECT BOMUNITID
            FROM InventTable
            WHERE ITEMID = ?
            """, PN)
        unit.append(cursor.fetchall()[
                    0][0])  # check with 148-0102-017 #######################
    return unit


def cleanZeroLevel(PN, AXconn):
    """
    Return clean dataframe of Zero level with descriptions in the following order
    PN, Unit, Qty, Description
    using my functions defined in CoilArt.py
    """
    with AXconn:
        PNs, Qty, Unit = Zero(AXconn, PN)
    df = pd.DataFrame({
        "PN": PNs,
        "Qty": Qty,
        "Unit": Unit
    })
    df = df.groupby(['PN', 'Unit']).sum()
    df.reset_index(level=['PN', 'Unit'], inplace=True)
    PNs = list(df.loc[:, 'PN'])
    with AXconn:
        Description = Name(AXconn, PNs)
    df['Description'] = Description
    return df


def Zero(conn, Item, Qty=1, Unit="EA"):
    PNList, BOMQTYList, UNITIDList = [], [], []
    PNcontainer, BOMQTYcontainer, UNITIDcontainer = Item_extract(conn, Item)
    if PNcontainer and BOMQTYcontainer and UNITIDcontainer:
        for (PN, BOMQTY, UNITID) in itertools.zip_longest(PNcontainer, BOMQTYcontainer, UNITIDcontainer):
            PNtmp, BOMQTYtmp, UNITIDtmp = Zero(conn, PN, 1, UNITID)
            if isinstance(PNtmp, list):
                PNList.extend(PNtmp)
                BOMQTYList.extend(i * BOMQTY for i in BOMQTYtmp)
                UNITIDList.extend(UNITIDtmp)
            elif isinstance(PNtmp, str):
                PNList.append(PNtmp)
                BOMQTYList.append(BOMQTYtmp * BOMQTY)
                UNITIDList.append(UNITIDtmp)
        return PNList, BOMQTYList, UNITIDList

    # DescriptionList = Name(conn, PNList)
    return Item, Qty, Unit


def Item_extract(conn, ITEMID, DF=False):
    BOMID = IsBOM(conn, ITEMID)
    PNcontainer, BOMQTYcontainer, UNITIDcontainer = [], [], []
    if BOMID:
        cursor = conn.cursor()

        if DF:
            cursor.execute("""
                SELECT ITEMID, BOMQTY, UNITID 
                FROM BOM 
                WHERE BOMID= ?""", BOMID)
            lines = cursor.fetchall()  # list of tuples
            LinesDF = pd.DataFrame.from_records(
                lines, columns=['PN', 'QTY', 'Unit'])
            return LinesDF

        cursor.execute("""
            SELECT ITEMID, BOMQTY, UNITID
            FROM BOM 
            WHERE BOMID= ?""", BOMID)
        lines = cursor.fetchall()  # list of tuples
        for PN, BOMQTY, UNITID in lines:
            PNcontainer.append(PN)
            BOMQTYcontainer.append(BOMQTY)
            UNITIDcontainer.append(UNITID)
        return PNcontainer, BOMQTYcontainer, UNITIDcontainer

    return None, None, None


def IsBOM(conn, ITEMID):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT BOMID
        FROM BOMVERSION
        WHERE ITEMID= ? AND ACTIVE=1 AND APPROVED=1""", ITEMID)
    BOMID = cursor.fetchall()
    if not BOMID:
        return None

    return BOMID[0][0]


def initmenu(ACCconn):
    """
    Return dict where keys are the Selector ID and values are options list.
    """
    menu = dict()
    with ACCconn:
        # FTPattern menu
        cur = ACCconn.cursor()
        cur.execute("SELECT DISTINCT Pattern FROM FinPress;")
        data = cur.fetchall()  # list of tuples
        FTPattern = pd.DataFrame.from_records(
            data, columns=['FTPattern'])
        # FTDiameter menu
        cur.execute("SELECT DISTINCT Diameter FROM FinPress;")
        data = cur.fetchall()  # list of tuples
        FTDiameter = pd.DataFrame.from_records(
            data, columns=['FTDiameter'])

    menu["FTPattern"] = list(FTPattern["FTPattern"].values.tolist())
    menu["FTDiameter"] = list(FTDiameter["FTDiameter"].values.tolist())

    return menu


def std_cost(ACCconn, PN):
    """
    Return direct mateial standard cost of one item or list of items
    """
    with ACCconn:
        cur = ACCconn.cursor()
        cur.execute("""
            SELECT Unit, V_price, V_Currency, 
            Bank_Charge_Percentage, Customs_Percentage, 
            Clearnace, Frieght, Frieght_Currency, Insurance, 
            Insurance_Currency, eight_Percent, Others_Percent, Volume 
            FROM DMCStandard WHERE PN= ?""", PN)
        data = cur.fetchall()  # list of tuples
    [(Unit, V_price, V_Currency,
      Bank_Charge_Percentage, Customs_Percentage,
      Clearnace, Frieght, Frieght_Currency, Insurance,
      Insurance_Currency, eight_Percent, Others_Percent, Volume)] = data
    print(data)
    TotalLandedCost = ((V_price*(1+Bank_Charge_Percentage)*(1+Customs_Percentage))
                       * exchange_rate(V_Currency)) + (Clearnace/Volume) + (Frieght*exchange_rate(Frieght_Currency)/Volume) + ((Insurance*exchange_rate(Insurance_Currency))/Volume) + (eight_Percent+Others_Percent)

    details = {"Unit": Unit,
               "V_price": V_price,
               "V_Currency": V_Currency,
               "Bank_Charge_Percentage": Bank_Charge_Percentage,
               "Customs_Percentage": Customs_Percentage,
               "Clearnace": Clearnace,
               "Frieght": Frieght,
               "Frieght_Currency": Frieght_Currency,
               "Insurance": Insurance,
               "Insurance_Currency": Insurance_Currency,
               "eight_Percent": eight_Percent,
               "Others_Percent": Others_Percent,
               "Volume": Volume}
    return TotalLandedCost, Unit, details


def exchange_rate(Currency):
    if Currency == "EUR":
        return 18.55
    elif Currency == "EGP":
        return 1
    elif Currency == "USD":
        return 15.74


def avg_cost(conn, PN):
    with conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT TOP 1 INVENTTRANS.COSTAMOUNTPOSTED/INVENTTRANS.QTY
            FROM INVENTTRANS 
            INNER JOIN INVENTTRANSORIGIN ON 
            INVENTTRANS.ITEMID = INVENTTRANSORIGIN.ITEMID AND 
            INVENTTRANS.INVENTTRANSORIGIN = INVENTTRANSORIGIN.RECID 
            LEFT OUTER JOIN INVENTDIM ON 
            INVENTTRANSORIGIN.ITEMINVENTDIMID = INVENTDIM.INVENTDIMID AND 
            INVENTTRANS.INVENTDIMID = INVENTDIM.INVENTDIMID
            WHERE INVENTTRANS.ITEMID = ?
            AND INVENTTRANSORIGIN.REFERENCECATEGORY= 7
            AND INVENTTRANS.STATUSRECEIPT = 1
            ORDER BY INVENTTRANS.DATEFINANCIAL DESC""", PN)
        data = cur.fetchall()
    return data[0]


def pur_cost(AXconn, PN):
    with AXconn:
        cur = AXconn.cursor()
        cur.execute("""
            SELECT TOP 1 INVENTTRANS.COSTAMOUNTPOSTED/INVENTTRANS.QTY
            FROM INVENTTRANS 
            INNER JOIN INVENTTRANSORIGIN 
            ON INVENTTRANS.ITEMID = INVENTTRANSORIGIN.ITEMID 
            AND INVENTTRANS.INVENTTRANSORIGIN = INVENTTRANSORIGIN.RECID 
            LEFT OUTER JOIN INVENTDIM 
            ON INVENTTRANSORIGIN.ITEMINVENTDIMID = INVENTDIM.INVENTDIMID
            AND INVENTTRANS.INVENTDIMID = INVENTDIM.INVENTDIMID
            WHERE INVENTTRANS.ITEMID = ?
            AND INVENTTRANSORIGIN.REFERENCECATEGORY= 3
            ORDER BY INVENTTRANS.DATEFINANCIAL DESC""", PN)
        data = cur.fetchall()
    return data[0]
