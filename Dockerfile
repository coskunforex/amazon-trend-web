# Basit ve güvenli tek aşama
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Matplotlib ve Pillow için gerekli sistem kütüphaneleri
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bağımlılıkları kur
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Uygulama kodu
COPY . .

# Port ve giriş
EXPOSE 8000
# Flask app nesnesi: app.server.app:app  (projendeki dosya/nesne) 
CMD ["gunicorn", "app.server.app:app", "-b", "0.0.0.0:8000", "-w", "2", "-k", "gthread", "--threads", "8"]
