import pandas as pd
import pyodbc


def Item_extract(conn, ITEMID):
    """
    Description: Get Lines and BOMs in zero level 

    Inputs: 
    conn    database connection object 
    ITEMID  input of item of interest 

    Outputs:
    LinesDF  Lines at zero level 
    BOMDF    BOMs at zero level 
    """

    BOMID = IsBOM(conn, ITEMID)
    # print(BOMID)
    if BOMID:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ITEMID, BOMQTY, UNITID 
            FROM BOM 
            WHERE BOMID= ?""", BOMID)
        lines = cursor.fetchall()
        LinesDF = pd.DataFrame.from_records(
            lines, columns=['PN', 'QTY', 'Unit'])
        return LinesDF

    return None


def IsBOM(conn, ITEMID):
    """
    Description: get the active version of input ITEMID

    Inputs: 
    conn    database connection object (type database)
    ITEMID  input of item of interest (type string)

    Outputs:
    BOMID   The active version of ITEMID (type cell)
    if ITEMID is not BOM or doesn't have active version, return None
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT BOMID
        FROM BOMVERSION
        WHERE ITEMID= ? AND ACTIVE=1 AND APPROVED=1""", ITEMID)
    BOMID = cursor.fetchall()
    if not BOMID:
        return None

    return BOMID[0][0]
