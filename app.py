from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")

    if not file or not allowed(file.filename):
        return "Só imagens (png/jpg)"

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # DEBUG: confirma arquivo existe
    if not os.path.exists(path):
        return "Erro ao salvar imagem"

    try:
        # abre imagem (Pillow :contentReference[oaicite:1]{index=1})
        img = Image.open(path)

        # pré-processamento forte (melhora OCR)
        img = img.convert("L")
        img = img.point(lambda x: 0 if x < 140 else 255, "1")

    except Exception as e:
        return f"Erro abrindo imagem: {str(e)}"

    try:
        # OCR (Tesseract :contentReference[oaicite:2]{index=2})
        text = pytesseract.image_to_string(img)

        if not text.strip():
            return "OCR não conseguiu ler texto (imagem ruim ou baixa qualidade)"

        return f"<pre>{text}</pre>"

    except Exception as e:
        return f"Erro no OCR: {str(e)}"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
