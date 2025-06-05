FROM python:3.11-slim

WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Unit-Tests ausführen
RUN python -m unittest discover -v -s tests -p "test*.py"

EXPOSE 3000

# Nur 1 Worker, preload damit Modell geteilt wird
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000"]
