#autor Gunaratne U.A
# pip install -r ../Mask_RCNN/requirements.txt
# All imports

import ipykernel
import sys
import os
import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, io, img_as_ubyte
from skimage.filters import threshold_multiotsu
from skimage.color import rgb2gray
from mrcnn.m_rcnn import *
from mrcnn.visualize import random_colors, get_mask_contours, draw_mask

image_save_path = "./assets/output/"

def prediction_disease(image_result, clinical_result):
    result = 0
    
    if (image_result == "tb"):
        result= result+2
    elif(image_result == "ic"):
        result= result-2
    elif(image_result == "normal"):
        result= result
        
    if (clinical_result == "tb"):
        result= result +1
    elif(clinical_result == "ic"):
        result= result-1
    elif(clinical_result == "normal"):
        result= result
        
    if(result>0):
        return "tb"
    elif(result<0):
        return "ic"
    elif(result == 0):
        return "normal"

#pre process image reduse the noise of the image 
def denoise_image(image_path , img_name):
    read_image = cv2.imread(image_path, 1)
    print(read_image)

    gaussian_image = cv2.GaussianBlur(read_image, (3, 3), 0)
    plt.imsave(image_save_path + "gaussian_output.png", gaussian_image)

    median_image = cv2.medianBlur(read_image, 3)
    plt.imsave(image_save_path + "median_output.png", median_image)
    return gaussian_image;


#threshold the image for model
def masdetection_image(gaussian_image):
    image_output_image = "./assets/output/MasDetection.png"

    # image = cv2.imread(image_path, 1)
    # # image = io.imread(file)
    # print(image)
    # plt.imshow(image, cmap="gray")
    # plt.show()

    image = rgb2gray(gaussian_image)
    threshold = threshold_multiotsu(image, classes=5)

    regions = np.digitize(image, bins=threshold)

    mas_image = img_as_ubyte(regions)
    plt.imsave(image_output_image, mas_image)
    return mas_image

#disease area identification in tb
def get_tb_segmantation(image_path ,TB_MODEL_PATH):
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
        contours = get_mask_contours(mask)
        for cnt in contours:
            cv2.polylines(img, [cnt], True, colors[i], 2)
            img = draw_mask(img, [cnt], colors[i])
    # cv2.Waitkey(10000)
    # cv2.imshow("img",img)
    plt.imsave("step1_tb_output.png", img)
    return img

#disease area identification in lc
def get_lc_segmantation(image_path ,LC_MODEL_PATH):
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
        contours = get_mask_contours(mask)
        for cnt in contours:
            cv2.polylines(img, [cnt], True, colors[i], 2)
            img = draw_mask(img, [cnt], colors[i])
    # cv2.Waitkey(10000)
    # cv2.imshow("img",img)
    plt.imsave(image_save_path+"step1_tb_output.png", img)
    return img
