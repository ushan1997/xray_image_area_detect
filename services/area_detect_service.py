from cgitb import reset
from unittest import result
import tensorflow as tf
from services.utiils import *

print("############# Runing on tensorflow ",
      tf.__version__, " backend.###################")

TB_MODEL_PATH = "./model/tuberculosis/tb_model_v8.h5"
LC_MODEL_PATH = "./model/lung_cancer/lc_model_v6.h5"


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
