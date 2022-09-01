#autor Gunaratne U.A
# pip install -r ../Mask_RCNN/requirements.txt

# All imports
import ipykernel
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

sys.path.append("../Mask_RCNN/mrcnn")
from m_rcnn import *
from visualize import random_colors, get_mask_contours, draw_mask

import tensorflow as tf 
print(tf.__version__)

# dataset anotations
# train_annotations_path = "../dataset/tb_dataset_v6/train.json"
# val_annotations_path = "../dataset/tb_dataset_v6/test.json"

# # Dataset load
# dataset_train = load_image_dataset(os.path.join( train_annotations_path), "../dataset/tb_dataset_v6/train", "train")
# dataset_val = load_image_dataset(os.path.join( val_annotations_path), "../dataset/tb_dataset_v6/test", "val")
# class_number = dataset_train.count_classes()

# print("Classes: {}".format(class_number))

def get_image(image_path , img_name):
    print(image_path)
    print("in method----------------------------")
    img = cv2.imread(image_path)


    test_model, inference_config = load_inference_model(1, "../models/tuberculosis/tb_model_v8.h5")
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
    # print(image)