FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libfreetype6 libjpeg62-turbo libpng16-16 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Daha net loglar için access & error logfile açtık, düşük RAM için 1 worker / 2 thread.
# Shell-form ile ${PORT} genişliyor.
CMD ["/bin/sh","-c","gunicorn app.server.app:app -w 1 -k gthread --threads 2 --worker-tmp-dir /dev/shm -b 0.0.0.0:${PORT} --timeout 120 --access-logfile - --error-logfile - --log-level info"]
