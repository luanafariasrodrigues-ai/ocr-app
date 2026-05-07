from flask import Flask, request, jsonify, render_template
import easyocr
import os
from PIL import Image

app = Flask(__name__)

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(
            ['pt', 'en'],
            model_storage_directory='/tmp/easyocr',
            gpu=False,
            verbose=False
        )
    return _reader

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        file = request.files['image']
        path = f"/tmp/{file.filename}"
        file.save(path)

        img = Image.open(path)
        img.thumbnail((1200, 1200))
        img.save(path)

        reader = get_reader()
        result = reader.readtext(path, detail=0)
        text = '\n'.join(result)

        os.remove(path)
        return jsonify({'text': text})

    except Exception as e:
        print(f"OCR ERROR: {e}")
        return jsonify({'text': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
