FROM python:3.11-slim

WORKDIR /app

# 1) requirements.txt kopieren
COPY requirements.txt ./

# 2) CPU-only Torch installieren
RUN pip install --no-cache-dir \
      torch==2.7.0+cpu \
      -f https://download.pytorch.org/whl/cpu/torch_stable.html \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download de_core_news_sm

COPY . .

ENV TOKENIZERS_PARALLELISM=false \
    PYTHONUNBUFFERED=1

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000", "--workers", "1", "--preload"]
