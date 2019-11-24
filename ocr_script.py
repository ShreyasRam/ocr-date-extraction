#this is the python file that the flask imports- calls parse_date()function 

import re
import os
import json
import pytesseract
from PIL import Image
from datetime import datetime
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import dateparser
from tqdm import tqdm
import requests 
from io import BytesIO
from preprocess import process_image_for_ocr


def find_date(regex, text):
    
    dt = re.findall(regex, text)
    if len(dt) > 0:
        for dt_obj in dt:
            print(dt)
            try:
                parsed_date = dateparser.parse(dt_obj)
                date_to_string = parsed_date.strftime('%Y-%m-%d')
                return date_to_string
            
            except:
                print(dt_obj,'is not in a correct date format!')

def parse_date(img_url):

    # v = Image.fromarray(gray)
    # response = requests.get(img_url)
    # unproc_img = Image.open(BytesIO(response.content))
    # proc_img = process_image_for_ocr(img_url)
    # img = Image.fromarray(proc_img)
    img = Image.open(img_url)
    text = pytesseract.image_to_string(img, config='') 
    

#     print(text)
    regex_1 = r'\d{1,2}[-/., ][a-zA-z0-9]+[,-/.\' ]\d{2,4}'
    regex_2 = r'\w+\s?\d{1,2}[,\']\s*\d{2,4}'
    
    ext_date = find_date(regex_1, text)

    if ext_date:
        return ext_date
    
    else:
        ext_date = find_date(regex_2, text)
        return ext_date