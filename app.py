from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import pdf2image
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configure Tesseract to use Arabic language
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update this path to where Tesseract is installed

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error('No file part in request.')
        return jsonify(error='No file part'), 400

    file = request.files['file']

    if file.filename == '':
        app.logger.error('No selected file.')
        return jsonify(error='No selected file'), 400

    if file and allowed_file(file.filename):
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)

        try:
            extracted_text = process_file(filepath)
        except Exception as e:
            app.logger.error(f'Error processing file: {e}')
            return jsonify(error='Error processing file'), 500
        finally:
            os.remove(filepath)  # Clean up the uploaded file after processing
        return jsonify(text=extracted_text)

    app.logger.error('File type not allowed.')
    return jsonify(error='File type not allowed'), 400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'pdf'}


def process_file(filepath):
    _, file_extension = os.path.splitext(filepath)
    text = ''

    if file_extension.lower() == '.pdf':
        images = pdf2image.convert_from_path(filepath)
        for image in images:
            text += pytesseract.image_to_string(image, lang='ara') + '\n'
    else:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image, lang='ara')

    return text

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
