# autor Gunaratne U.A
# pip install -r ../Mask_RCNN/requirements.txt
# All imports

from flask import send_file
import ipykernel
import sys
import os
import cv2
import glob
import json
from json import JSONEncoder
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, io, img_as_ubyte
from skimage.filters import threshold_multiotsu
from skimage.color import rgb2gray
from mrcnn.m_rcnn import *
from PIL import Image
from mrcnn.visualize import random_colors, get_mask_contours, draw_mask

image_save_path = "./assets/output/"

#predecting disease
def prediction_disease(image_result, clinical_result):
    result = 0

    if (image_result == "tb"):
        result = result+2
    elif (image_result == "lc"):
        result = result-2
    elif (image_result == "normal"):
        result = result

    if (clinical_result == "tb"):
        result = result + 1
    elif (clinical_result == "lc"):
        result = result-1
    elif (clinical_result == "normal"):
        result = result

    if (result > 0):
        return "tb"
    elif (result < 0):
        return "lc"
    elif (result == 0):
        return "normal"

# pre process image reduse the noise of the image
def denoise_image(image_path, img_name):
    print("####### denoise the image ########")
    image_output_path = "./assets/output/denoise_image.png"
    read_image = cv2.imread(image_path, 1)
    print(read_image)

    median_image = cv2.medianBlur(read_image, 3)
    plt.imsave(image_output_path, median_image)
    return image_output_path

# threshold the image for model
def masdetection_image(image_path, img_name):
    print("####### masdetection_image the image ########")
    image_output_path = "./assets/output/masdetection_image.png"
    image_400_path = "./assets/output/image_400.png"
    read_image = cv2.imread(image_path, 1)
    print(read_image)

    rgb2gray_image = rgb2gray(read_image)
    threshold = threshold_multiotsu(rgb2gray_image, classes=5)

    regions = np.digitize(rgb2gray_image, bins=threshold)

    mas_image = img_as_ubyte(regions)
    plt.imsave(image_output_path, mas_image)
    
    image = Image.open(image_output_path)
    print(f"Original size : {image.size}") # 5464x3640

    sunset_resized = image.resize((400, 400))
    sunset_resized.save(image_400_path)
    return image_400_path

# disease area identification in tb
def get_tb_segmantation(image_path, TB_MODEL_PATH):
    print("###### stared instance segmantation #######")
    poly_array=[]
    image_output_path = "./assets/output/tb_output.png"
    
    img = cv2.imread(image_path)
    test_model, inference_config = load_inference_model(1, TB_MODEL_PATH)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect results
    r = test_model.detect([image])[0]
    colors = random_colors(80)

    # Get Coordinates and show it on the image
    object_count = len(r["class_ids"])
    for i in range(object_count):
        # 1. Mask
        mask = r["masks"][:, :, i]
        #get polygons of the masks
        contours = get_mask_contours(mask)
        #add contours to poly_array
        poly_array.append(contours)
        print("contours======>",contours)

        for cnt in contours:
            cv2.polylines(img, [cnt], True, (255, 0, 0), 2)
            img = draw_mask(img, [cnt], (255, 0, 0))
    # cv2.Waitkey(10000)
    # cv2.imshow("img",img)
    plt.imsave(image_output_path, img)
    save_polygon_as_json(poly_array)
    return image_output_path

# disease area identification in lc
def get_lc_segmantation(image_path, LC_MODEL_PATH):
    poly_array=[]
    image_output_path = "./assets/output/lc_output.png"

    img = cv2.imread(image_path)
    test_model, inference_config = load_inference_model(1, LC_MODEL_PATH)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect results
    r = test_model.detect([image])[0]
    colors = random_colors(80)

    # Get Coordinates and show it on the image
    object_count = len(r["class_ids"])
    for i in range(object_count):
        # 1. Mask
        mask = r["masks"][:, :, i]
        #get polygons of the masks
        contours = get_mask_contours(mask)
        #add contours to poly_array
        poly_array.append(contours)
        print("contours======>",contours)
        for cnt in contours:
            cv2.polylines(img, [cnt], True, (255, 0, 0), 2)
            img = draw_mask(img, [cnt], (255, 0, 0))
    # cv2.Waitkey(10000)
    # cv2.imshow("img",img)
    #image save 
    plt.imsave(image_output_path, img)
    save_polygon_as_json(poly_array)
    return image_output_path

# save polygon as json
def save_polygon_as_json(poly_array):
    print("###### stared save polygon to json #######")
    json_output_path = "./assets/output/output.json"

    class NumpyArrayEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)

    # Serialization
    numpyData = {"array": poly_array}
    # use dump() to write array into file
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
    print("Printing JSON serialized NumPy array")
    print(encodedNumpyData)

    with open(json_output_path, 'w') as outfile:
        json.dump(encodedNumpyData, outfile)

# get mask cordinates for augmnted reality
def get_mask(json_path, bulb_cordinates):
    print("###### stared save polygon to json #######")
    with open(json_path) as json_file:
        data = json.load(json_file)
        decodedArrays = json.loads(data)
        array = np.asarray(decodedArrays["array"])

        bulb_arr = bulb_cordinates

        cod_json = []
        #bulb cordinates populate
        if(len(bulb_arr)>0):
            for l in range(len(bulb_arr)):
                #polygon array
                if(len(array)>0):
                    for i in range(len(array)):
                        for j in range(len(array[i])):
                            diff =[]
                            for k in range(len(array[i][j])):
                                #y value equalization
                                if(bulb_arr[l][1]== array[i][j][k][1]): 
                                    print("check y value same with polygon ",array[i][j][k])
                                    diff.append(array[i][j][k])
                                    if(len(diff)>0):
                                        length_diff = len(diff)
                                        #x value range check
                                        if diff[0][0] <= bulb_arr[l][0] <= diff[length_diff-1][0]:
                                            cod_json.append(bulb_arr[l])    

        print(cod_json)            
        #check duplicate cordinates
        set_bulb_arr = []
        for i in range(len(bulb_arr)):
            for j in range(len(cod_json)):
                if(bulb_arr[i]==cod_json[j]):
                    set_bulb_arr.append(i+1)

        mylist = sorted(set(set_bulb_arr))
        print(mylist)
    return mylist

