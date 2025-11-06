FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ghostscript poppler-utils \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir gunicorn

COPY . /app
RUN mkdir -p /app/data

EXPOSE 8000

# Démarre l'app Flask (module app.py avec app = Flask(__name__))
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers", "2", "--threads", "4", "--timeout", "120"]

