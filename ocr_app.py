import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, render_template
import base64
# from ocr_script import parse_date
app = Flask(__name__)
_VERSION = 1
from werkzeug.utils import secure_filename



uploads_dir = os.path.join(app.instance_path, 'bills')
os.makedirs(uploads_dir, exist_ok=True)
app.config['UPLOAD_FOLDER'] = uploads_dir

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# @app.route('')
# def index():
#     return render_template('upload.html')

@app.route('/ocr', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file: #and allowed_file(file.filename):
            f = os.path.join(uploads_dir, secure_filename(file.filename))
            file.save(f)
            # call the OCR function on it
            extracted_text = parse_date(file)

            img_type = os.path.splitext(f)[-1][1:]
            with open(f, "rb") as image_file:
                encoded_img = 'data:image/{};base64,'.format(img_type) + base64.b64encode(image_file.read()).decode('ascii')

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   picture = encoded_img,
                                   img_src= uploads_dir + file.filename )
            # return jsonify({"output": extracted_text})
    elif request.method == 'GET':
            return render_template('upload.html')


# @app.route('/'.format(_VERSION), methods=["POST"])
# def ocr():
    # # try:
    # img_url = request.json['image_url']
    
    # if img_url:

    #     output= parse_date(img_url)
    #     return jsonify({"output": output,
    #      # "parsed_date":d, "detected_objs":d_list
    #      })
    # else:
    #     return jsonify({"error": "only .jpg files, please"})
    # except:# Exception as e: 
    #     # print(e)
    #     return jsonify(
    #         {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
    #     )








if __name__ == "__main__":
    app.run(debug = True) 