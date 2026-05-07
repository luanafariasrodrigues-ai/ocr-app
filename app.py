import os
import cv2
import pytesseract
import numpy as np
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ocr", methods=["POST"])
def ocr():
    file = request.files.get("image")
    lang = request.form.get("lang", "por+eng")

    if not file:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    img_np = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    texto = pytesseract.image_to_string(thresh, lang=lang)

    return jsonify({"texto": texto.strip()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
