FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr \
    && which tesseract \
    && tesseract --version \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY Backend /app/Backend
COPY Frontend /app/Frontend

ENV PATH="/usr/bin:${PATH}"

WORKDIR /app/Backend

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]