from flask import Flask, render_template, request
import pytesseract
from PIL import Image, ImageEnhance
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")

    if not file:
        return "No file uploaded"

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    img = Image.open(path)
    img = ImageEnhance.Contrast(img).enhance(2)
    img = img.convert("L")

    text = pytesseract.image_to_string(img)

    return f"<pre>{text}</pre>"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
