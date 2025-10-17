# Basit ve güvenli tek aşama
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# (Matplotlib/Pillow gerekirse) sistem paketleri
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libfreetype6 libjpeg62-turbo libpng16-16 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bağımlılıklar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodu
COPY . .

# Render $PORT'u ENV olarak geçer; shell-form ile genişletiyoruz.
# Tek worker + 2 thread => düşük RAM, stabil
CMD ["/bin/sh", "-c", "gunicorn app.server.app:app -w 1 -k gthread --threads 2 --worker-tmp-dir /dev/shm -b 0.0.0.0:${PORT} --timeout 120"]
