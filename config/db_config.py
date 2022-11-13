import mysql.connector
import json

def create_con():
    MyDB = mysql.connector.connect(
    host="127.0.0.2",
    user="root",
    password="root",
    database="cxr_scan"
    )
    return MyDB

def insert(sql_query, args):
    db = create_con()
    cursor = db.cursor()
    try:
        cursor.execute(sql_query, args)
        db.commit()
        db.close()
        return args
    except Exception as e:
        db.rollback()
        db.close()
        print(e)
        return e
