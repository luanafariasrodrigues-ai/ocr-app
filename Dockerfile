FROM python:3.11-slim

# instala dependências do sistema + tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# importante pro Render
ENV PORT=10000

CMD ["python", "app.py"]
