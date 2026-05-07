from flask import Flask, request, jsonify, render_template
import easyocr
import os

app = Flask(__name__)
reader = easyocr.Reader(['pt', 'en'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files['image']
    path = f"temp_{file.filename}"
    file.save(path)

    result = reader.readtext(path)
    text = '\n'.join([text for (_, text, _) in result])

    os.remove(path)
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
