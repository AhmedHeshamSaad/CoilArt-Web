import pandas as pd
import pyodbc


class Item:
    def __init__(self, PN, Qty, UNITID, Parent, BOM=None):
        self.PN = PN
        self.UNITID = UNITID
        self.parent = Parent
        self.BOM = BOM


def Zero(conn, PN):
    List = []
    Lup = Item_extract(conn, PN)
    if Lup:
        for Item in Lup:
            tmp = Zero(conn, Item)
            if isinstance(tmp, list):
                List.extend(tmp)
            elif isinstance(tmp, str):
                List.append(tmp)
        return List
    return PN


def Item_extract(conn, ITEMID, DF=False):
    BOMID = IsBOM(conn, ITEMID)
    container = []
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
            SELECT ITEMID
            FROM BOM 
            WHERE BOMID= ?""", BOMID)
        lines = cursor.fetchall()  # list of tuples
        for PN in lines:
            container.append(PN[0])
        return container

    return None


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
