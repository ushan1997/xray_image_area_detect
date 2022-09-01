import glob
import os
import cv2
from matplotlib import pyplot as plt

image_path = "./images/tb0030.png"
image_save_path = "./output/"

read_image = cv2.imread(image_path, 1)
print(read_image)

gaussian_image = cv2.GaussianBlur(read_image, (3, 3), 0)
plt.imsave(image_save_path + "gaussian_output.png", gaussian_image)

median_image = cv2.medianBlur(read_image, 3)
plt.imsave(image_save_path + "median_output.png", median_image)
