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
