from cgitb import reset
from unittest import result
import tensorflow as tf 
from services.utiils import *

print("##############Runing on tensorflow ",tf.__version__," backend.###################")

TB_MODEL_PATH = "./model/tuberculosis/tb_model_v8.h5"
LC_MODEL_PATH = "./model/tuberculosis/lc_model_v6.h5"
image_output_image = "./assets/output/MasDetection.png"


def area_detect(image_result,clinical_result, image_path , img_name):
    FINAL_RESULT = prediction_disease(image_result,clinical_result)
    print(FINAL_RESULT)
    gaussian_image = denoise_image(image_path , img_name)
    masdetection_image(gaussian_image)
    if FINAL_RESULT == "tb":
        get_tb_segmantation(image_output_image,TB_MODEL_PATH)
    elif FINAL_RESULT == "lc" :
        get_lc_segmantation(image_output_image,LC_MODEL_PATH)

   
