# @author Gunaratne U.A
# @email it19753140@my.sliit.lk
# 
from flask import Flask, render_template,  request,make_response,jsonify
from werkzeug.utils import secure_filename
import os
import sys
from services.query_service import *
from services.area_detect_service import *

app = Flask(__name__)

UPLOAD_FOLDER = 'assets/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/areadt/testapi', methods = ['GET'])
def test_api():
   return "server started ."

@app.route('/areadt/getimage' ,methods = ['GET'])
def get_image():
   return "dsf"

@app.route('/areadt/processimage', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      # create a secure filename
      filename = secure_filename(file.filename)
      print("filename======>",filename)
      # save file to /static/uploads
      filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      print(filepath)
      file.save(filepath)
      area_detect(image_result="tb",clinical_result="tb",image_path=filepath,img_name=filename)
      # get_image(filepath, filename)
      return "file saveds"
      # return render_template("uploaded.html", display_detection = filename, fname = filename)      

@app.route("/insert", methods=["POST"])
def insert():
    data = request.get_json()
    print("Json Obj",data)
    name = data["name"]
    print("name",name)
    result = save_activity_details((name,))
    return make_response(jsonify({"name": result}),200)

if __name__ == '__main__':
   app.run(port=6000, debug=True)
