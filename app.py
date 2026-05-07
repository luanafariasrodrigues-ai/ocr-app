from flask import Flask, request, jsonify, render_template
import easyocr
import os

app = Flask(__name__)

# Load reader only once, outside of requests
_reader = None

def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['pt', 'en'], 
                          model_storage_directory='/tmp/easyocr',
                          gpu=False)  # Render free tier has no GPU
    return _reader

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files['image']
    path = f"/tmp/{file.filename}"
    file.save(path)

    reader = get_reader()
    result = reader.readtext(path)
    text = '\n'.join([text for (_, text, _) in result])

    os.remove(path)
    return jsonify({'text': text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
