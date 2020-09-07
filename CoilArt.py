import pandas as pd
import pyodbc
import itertools


class Item:
    def __init__(self, PN, Qty, UNITID, Parent, BOM=None):
        self.PN = PN
        self.UNITID = UNITID
        self.parent = Parent
        self.BOM = BOM


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
