from flask import Flask, request, jsonify, render_template
import easyocr
import os

app = Flask(__name__)

# Fix 1: store models in /tmp to avoid permission errors
reader = easyocr.Reader(['pt', 'en'], model_storage_directory='/tmp/easyocr')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files['image']
    
    # Fix 2: save temp files in /tmp
    path = f"/tmp/{file.filename}"
    file.save(path)

    result = reader.readtext(path)
    text = '\n'.join([text for (_, text, _) in result])

    os.remove(path)
    return jsonify({'text': text})

if __name__ == '__main__':
    # Fix 3: use Render's PORT and host 0.0.0.0
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
