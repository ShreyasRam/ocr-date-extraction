import re
import pytesseract
from PIL import Image
from PIL import ImageFile
import dateutil.parser

ImageFile.LOAD_TRUNCATED_IMAGES = True

def find_date(regex, text):

    dt = re.findall(regex, text)
    dt = [x.strip(' ') for x in dt]
    if len(dt) > 0:
        for dt_obj in dt:
            try:
                parsed_date = dateutil.parser.parse(dt_obj, dayfirst=True).strftime('%Y-%m-%d')

                return parsed_date

            except:
                print(dt_obj,'is not in a correct date format!')

def parse_date(img):

    text = pytesseract.image_to_string(img, config='')

    regex_1 = r'\d{1,2}[-/.,][a-zA-z0-9]+[,-/.\']\d{2,4}'
    regex_2 = r'\w+\s?\d{1,2}[,\']\s*\d{2,4}'

    ext_date = find_date(regex_1, text)

    if ext_date:
        return ext_date

    else:
        ext_date = find_date(regex_2, text)
        return ext_date
