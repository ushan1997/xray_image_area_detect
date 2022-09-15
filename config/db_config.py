import mysql.connector
import json

def create_con():
    db = mysql.connector.connect(
        database="cxr_scan",
        host="localhost",
        user="root",
        password="root"
    )
    return db

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
