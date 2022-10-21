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

app = Flask(__name__)

UPLOAD_FOLDER = 'assets/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/areadt/testapi', methods=['GET'])
def test_api():
    return jsonify({
        "message": "server started .",
        "code":200,
        "resourse": 1
    })

@app.route('/areadt/processimage', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            # create a secure filename
            image_result = request.form['image_result']
            clinical_result = request.form['clinical_result']

            filename = secure_filename(file.filename)
            # save file to /static/uploads
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            file.save(filepath)
            final_disease_result = prect_disease(
                image_result=image_result, clinical_result=clinical_result)
            image_output_path = area_detect(
                final_disease_result=final_disease_result, image_path=filepath, img_name=filename)
            print(image_output_path)
            fileImage = image_output_path
            image = open(fileImage, 'rb')
            image_read = image.read()
            image_64_encode = base64.encodebytes(image_read)
            utfResult = image_64_encode.decode("utf-8")
            # return json.dumps(str(utfResult.strip()))
            return jsonify({
                "message": "Image processed sucessfully",
                "code":200,
                "resourse": str(utfResult.strip())
            })
        except:
            jsonify({
                "message": "Something went wrong",
                "code":500,
                "resourse": ""
            })


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
    # print(json.dumps(data))
    # return json.dumps(data)


@app.route('/areadt/identify', methods=['POST'])
def identify_disease():
    image_result = request.form['image_result']
    clinical_result = request.form['clinical_result']
    return prect_disease(image_result=image_result, clinical_result=clinical_result)


@app.route("/insert", methods=["POST"])
def insert():
    data = request.get_json()
    print("Json Obj", data)
    name = data["name"]
    print("name", name)
    result = save_activity_details((name,))
    return make_response(jsonify({"name": result}), 200)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
