import os
import base64
from PIL import Image
from ocr_script import parse_date
from werkzeug.utils import secure_filename
from preprocess import process_image_for_ocr
from flask import Flask, request, render_template

_VERSION = 1

uploads_dir = os.path.join(app.instance_path, 'bills')
os.makedirs(uploads_dir, exist_ok=True)
app.config['UPLOAD_FOLDER'] = uploads_dir

ALLOWED_EXTENSION = ['jpg','png','jpeg']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        image = request.files['file']
        
        # if no file is selected 
        if image.filename == '':
            return render_template('upload.html', msg='No file selected')
        
        if image.filename.split(".")[1] not in ALLOWED_EXTENSION:
            return render_template('upload.html', msg='Incorrect Image Format')
        
        if image:
            f = os.path.join(uploads_dir, secure_filename(image.filename))
            image.save(f)
            
            # call the OCR function on it
            extracted_text = parse_date(f)
            if extracted_text == None:
                image_arr = process_image_for_ocr(f)
                proc_image = Image.fromarray(image_arr)

                extracted_text = parse_date(proc_image)

            img_type = os.path.splitext(f)[-1][1:]

            #encoding image to base64
            with open(f, "rb") as image_file:
                encoded_img = 'data:image/{};base64,'.format(img_type) + base64.b64encode(image_file.read()).decode('ascii')

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   picture = encoded_img,
                                   img_src= f)

    elif request.method == 'GET':
            return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug = True)
