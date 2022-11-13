# @author Gunaratne U.A
# @email it19753140@my.sliit.lk
#
from flask import Flask, render_template,  request, make_response, jsonify, Response
from werkzeug.utils import secure_filename
import os
import sys
from services.query_service import *
from services.area_detect_service import *
import json
import base64
import mysql.connector
from config.db_config import *

app = Flask(__name__)

UPLOAD_FOLDER = 'assets/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# api for test the application
@app.route('/areadt/testapi', methods=['GET'])
def test_api():
    return jsonify({
        "message": "server started .",
        "code": 200,
        "resourse": 1
    })

# api for get the disese spread area
@app.route('/areadt/processimage', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            # get request parameters
            file = request.files['file']
            image_result = request.form['image_result']
            clinical_result = request.form['clinical_result']

            # get image file name and image path and save
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded.png")
            file.save(filepath)

            # predict the disease type
            final_disease_result = prect_disease(
                image_result=image_result, clinical_result=clinical_result)

            image_output_path = area_detect(
                final_disease_result=final_disease_result, image_path=filepath, img_name="uploaded.png")
            print(image_output_path)
            fileImage = image_output_path
            image = open(fileImage, 'rb')
            image_read = image.read()
            image_64_encode = base64.encodebytes(image_read)
            utfResult = image_64_encode.decode("utf-8")
            # return json.dumps(str(utfResult.strip()))
            return jsonify({
                "message": "Image processed sucessfully",
                "code": 200,
                "resourse": str(utfResult.strip())
            })
        except:
            jsonify({
                "message": "Something went wrong",
                "code": 500,
                "resourse": ""
            })

# api for get the disese spread area in utf
@app.route('/areadt/processimageinutf', methods=['GET', 'POST'])
def upload_file_utf():
    if request.method == 'POST':
        try:
            # get request parameters
            file = request.form['file']
            image_result = request.form['image_result']
            clinical_result = request.form['clinical_result']

            # get image file name and image path and save
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded.png")
            file.save(filepath)

            # predict the disease type
            final_disease_result = prect_disease(
                image_result=image_result, clinical_result=clinical_result)

            image_output_path = area_detect(
                final_disease_result=final_disease_result, image_path=filepath, img_name="uploaded.png")
            print(image_output_path)
            fileImage = image_output_path
            image = open(fileImage, 'rb')
            image_read = image.read()
            image_64_encode = base64.encodebytes(image_read)
            utfResult = image_64_encode.decode("utf-8")
            # return json.dumps(str(utfResult.strip()))
            return jsonify({
                "message": "Image processed sucessfully",
                "code": 200,
                "resourse": str(utfResult.strip())
            })
        except Exception as e:
            jsonify({
                "message": str(e),
                "code": 500,
                "resourse": ""
            })

# api for get the spreded area masks
@app.route('/areadt/getmask', methods=['GET'])
def get_mask():
    try:
        bulb_arr = get_mask_service()
        return jsonify({
            'message': "OK",
            'code': 200,
            'resourse': bulb_arr,
        })
    except Exception as e:
        jsonify({
            "message": str(e),
            "code": 500,
            "resourse": ""
        })

# api for test image convert t base64 string
@app.route('/areadt/image', methods=['POST'])
def get_file():
    fileImage = "./assets/output/lc_output.png"
    image = open(fileImage, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodebytes(image_read)
    utfResult = image_64_encode.decode("utf-8")
    print(str(utfResult.strip()))
    # return json.dumps(str(utfResult.strip()))
    return jsonify({
        "message": "Image processed sucessfully",
        "disease": str(utfResult.strip())
    })

# api for insert image to db
@app.route('/areadt/insertimage', methods=['GET', 'POST'])
def db_upload_file():
    if request.method == 'POST':
        try:
            # get request parameters
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            disease = request.form['disease']

            MyDB = create_con()
            myCursor = MyDB.cursor()

            # myCursor.execute("CREATE TABLE IF NOT EXISTS disease_images (id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY,image LONGBLOB NOT NULL")
            myCursor.execute(
                "CREATE TABLE IF NOT EXISTS disease_images (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,image LONGBLOB NOT NULL,disease VARCHAR(255))")
            with open(filepath, 'rb') as File:
                BinaryData = File.read()

            selectSQLQry = "SELECT * FROM disease_images"
            myCursor.execute(selectSQLQry)
            myResult = myCursor.fetchall()

            if(len(myResult)>0):
                updateSQLQry = "UPDATE disease_images SET image =  %s, disease =%s WHERE id = 1"
                val = (BinaryData, disease)
                myCursor.execute(updateSQLQry, val)
                MyDB.commit()
            else:
                 insertSQLQry = "INSERT INTO disease_images (image,disease) VALUES (%s, %s)"
                 val = (BinaryData, disease)
                 myCursor.execute(insertSQLQry, val)
                 MyDB.commit()

            # SQLState2 = "SELECT * FROM disease_images WHERE id='{0}'"
            # myCursor.execute(SQLState2.format(str(1)))
            # myResult = myCursor.fetchone()[1]
            # print(myResult)
            # storeFilePath = "assets/output/img{0}.png".format(str(1))
            # with open(storeFilePath,'wb') as File:
            #     File.write(myResult)
            #     File.close()
            myCursor.close()
            return jsonify({
                "message": "Image Inserted sucessfully",
                 "code": 200,
            })

        except Exception as e:
            jsonify({
                "message": str(e),
                "code": 500,
            })

# api for get image to db
@app.route("/areadt/getimage", methods=['GET'])
def get_images_from_db():
    try:
        MyDB = create_con()
        myCursor = MyDB.cursor()
        selectSQLQry = "SELECT * FROM disease_images"
        myCursor.execute(selectSQLQry)
        data = myCursor.fetchall()
        image = data[0][1]
        disease =data[0][2]
        image_64_encode  = base64.encodebytes(image)
        utfResult = image_64_encode.decode("utf-8")
        myCursor.close()
        return jsonify({
            "code": 200,
            "image": str(utfResult.strip()),
            "disease":disease,
            "message": "Image processed sucessfully",
        })
    except Exception as e:
        jsonify({
            "code": 500,
            "image": "",
            "disease": "",
            "message": str(e)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
