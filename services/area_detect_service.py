# autor Gunaratne U.A
# pip install -r ../Mask_RCNN/requirements.txt
# All imports

from cgitb import reset
from unittest import result
import tensorflow as tf
from services.utiils import *

print("############# Runing on tensorflow ",
      tf.__version__, " backend.###################")

TB_MODEL_PATH = "./model/tuberculosis/tb_model_v8.h5"
LC_MODEL_PATH = "./model/lung_cancer/lc_model_v6.h5"

#bulb cordinates
bulb_cordinates=[
[50,50],[120,50],       [250,50],[300,50],[350,50],
[45,75],[75,75],[100,75],     [220,75],[240,75],[275,75],[320,75],[360,75],
[40,100],[45,100],[90,100],[110,100],      [210,100],[230,100],[275,100],[320,100],[360,100],
[35,125],[40,125],[60,125],[100,125],      [200,125],[220,125],[265,125],[310,125],[325,125],[365,125],
[25,150],[50,150],[75,150],[100,150],      [200,150],[240,150],[260,150],[300,150],[345,150],[367,150],
[23,175],[45,175],[65,175],[95,175],[120,175],    [210,175],[242,175],[265,175],[310,175],[355,175],[367,175],
[23,200],[45,200],[65,200],[95,200],[120,200],    [245,200],[265,200],[310,200],[355,200],[367,200],
[20,225],[50,225],[75,225],[100,225],[120,225],     [265,225],[310,225],[355,225],[367,225],
[17,250],[45,250],[55,250],[85,250],[100,250],[120,250],   [270,250],[310,250],[355,225],[367,225],
[25,300],[50,300],[75,300],[100,300],[100,250],       [275,250],[310,250],[355,225],[367,225],
[25,325],[50,325],[75,325],[100,325],[100,325],       [275,325],[310,325],[355,325],[367,325]
]

json_path = "./assets/output/output.json"

def prect_disease(image_result, clinical_result):
     final_disease_result = prediction_disease(image_result, clinical_result)
     print("final_disease_result",final_disease_result)
     return final_disease_result


def area_detect(final_disease_result, image_path, img_name):
    # preprocessing image
    denoised_image_path = denoise_image(image_path, img_name)
    masdetectioned_image_path = masdetection_image(denoised_image_path, img_name)

    if final_disease_result == "tb":
       image_output_path = get_tb_segmantation(masdetectioned_image_path, TB_MODEL_PATH)
    elif final_disease_result == "lc":
       image_output_path = get_lc_segmantation(masdetectioned_image_path, LC_MODEL_PATH)
    return image_output_path


def get_mask_service():
   bulb_arr = get_mask(json_path,bulb_cordinates)
   return bulb_arr