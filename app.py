from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# só imagens permitidas
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")

    # valida arquivo
    if not file or not allowed(file.filename):
        return "Só imagem (png/jpg)"

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # abre imagem (Pillow :contentReference[oaicite:1]{index=1})
    try:
        img = Image.open(path)
    except:
        return "Arquivo inválido"

    # OCR (Tesseract :contentReference[oaicite:2]{index=2})
    text = pytesseract.image_to_string(img)

    return f"<pre>{text}</pre>"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
