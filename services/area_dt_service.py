from config.db_config  import *
from flask import jsonify

def save_activity_details(name):
    qry = "INSERT INTO test (name) VALUES (%s)"
    args = (name)
    result = insert(qry, args)
    return result


def predictData(audioFile, name):


    new_predict_file_name = name.split(".")
    FPFN = new_predict_file_name[0]
