from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from PIL import Image
import os

app = Flask(__name__)
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        file = request.files['image']
        image = Image.open(file)
        response = model.generate_content(["Extract all text from this image:", image])
        return jsonify({'text': response.text})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({'text': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
