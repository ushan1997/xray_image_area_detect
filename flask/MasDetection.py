import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import glob
from skimage import data, io, img_as_ubyte
from skimage.filters import threshold_multiotsu
from skimage.color import rgb2gray, rgba2rgb

image_path = "./output/median_output.png"
image_output_image = "./output/MasDetection.png"

image = cv2.imread(image_path, 1)
# image = io.imread(file)
print(image)
plt.imshow(image, cmap="gray")
# plt.show()

image = rgb2gray(image)
threshold = threshold_multiotsu(image, classes=5)

regions = np.digitize(image, bins=threshold)

output = img_as_ubyte(regions)
plt.imsave(image_output_image, output)
