import os
from PIL import Image
from PIL import ImageFile 
ImageFile.LOAD_TRUNCATED_IMAGES = True
from tqdm import tqdm

import tempfile

import imutils
import requests 
import numpy as np
from io import BytesIO
import tempfile

# import cv2
import logging
import numpy as np
from PIL import Image

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

size = None


def get_size_of_scaled_image(im):
    global size
    if size is None:
        length_x, width_y = im.size
        factor = max(1, int(IMAGE_SIZE / length_x))
        size = factor * length_x, factor * width_y
    return size


def process_image_for_ocr(unproc_img):
    logging.info('Processing image for text Extraction')
    temp_filename = set_image_dpi(unproc_img)
    im_new = remove_noise_and_smooth(temp_filename)
    img = Image.fromarray(im_new)
    # gray = cv2.cvtColor(temp_filename, cv2.COLOR_BGR2GRAY)
    # gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # img_arr = cv2.medianBlur(gray, 5)
    return im_new


def set_image_dpi(unproc_img):
    # im = Image.open(file_path)
    response = requests.get(unproc_img)
    unproc_img = Image.open(BytesIO(response.content))
    im = unproc_img.convert('RGB')
    # size = (1800, 1800)
    size = get_size_of_scaled_image(im)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
#     im_path = os.path.join('/Users/shreyas/Datasets/',temp_filename.split(sep='/')[-1])
    im_resized.save(temp_filename, dpi=(300, 300))  # best for OCR
    return temp_filename


def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    logging.info('Removing noise and smoothening image')
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image