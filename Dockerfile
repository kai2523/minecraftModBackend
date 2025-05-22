FROM python:3.11-slim

WORKDIR /app

# Kopiere nur das requirements
COPY requirements.txt ./

# 1) CPU-only Torch aus dem PyTorch CPU-Index
RUN pip install --no-cache-dir \
      --index-url https://download.pytorch.org/whl/cpu \
      torch \
    # 2) Restliche Abhängigkeiten (ohne torch)
    && pip install --no-cache-dir -r requirements.txt \
    # 3) Spacy-Modell
    && python -m spacy download de_core_news_sm

COPY . .

ENV TOKENIZERS_PARALLELISM=false \
    PYTHONUNBUFFERED=1

# Nur 1 Worker, preload damit Modell geteilt wird
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000", "--workers", "1", "--preload"]
