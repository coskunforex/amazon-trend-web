# Deployment Yol Haritası (Sabit Omurga)
- Runtime: Python 3.11 (Linux/amd64)
- Paketleme: Docker (multi-stage)
- Veri: DuckDB + Parquet
- Proxy + TLS: Caddy (Let’s Encrypt)
- CI/CD: GitHub Actions → image → SSH deploy
- Konfig: .env / .env.prod
- İzleme: Sentry (errors), UptimeRobot (/health), günlük S3 yedek
- Sunucu: Remote VM (>= 4 vCPU / 8 GB RAM; ideal 8/16 + NVMe)
