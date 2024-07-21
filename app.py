from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import pdf2image
import os

app = Flask(__name__)

# Configure Tesseract to use Arabic language
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update this path to where Tesseract is installed

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error=No file part), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(error=No selected file), 400

    if file and allowed_file(file.filename):
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)

        extracted_text = process_file(filepath)
        os.remove(filepath)  # Clean up the uploaded file after processing
        return jsonify(text=extracted_text)

    return jsonify(error=File type not allowed), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'pdf'}

def process_file(filepath):
    _, file_extension = os.path.splitext(filepath)
    text = 

    if file_extension.lower() == .pdf:
        images = pdf2image.convert_from_path(filepath)
        for image in images:
            text += pytesseract.image_to_string(image, lang='ara') + n
    else:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image, lang='ara')

    return text

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
