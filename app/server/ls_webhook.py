# app/server/ls_webhook.py
import os, hmac, hashlib
from flask import Blueprint, request, jsonify
from app.server.emailing import send_pro_activated_email

ls_bp = Blueprint("ls_bp", __name__)
LS_SECRET = os.getenv("LEMON_WEBHOOK_SECRET", "")

def _verify_signature(raw: bytes, sig: str) -> bool:
    if not LS_SECRET:
        return True  # dev ortamında secret yoksa doğrulama atlanır
    mac = hmac.new(LS_SECRET.encode("utf-8"), msg=raw, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), (sig or "").strip())

@ls_bp.post("/webhooks/lemon")  # <-- İSTEDİĞİN ENDPOINT
def lemon_webhook():
    raw = request.data
    sig = request.headers.get("X-Signature", "")  # Lemon Squeezy'nin HMAC başlığı
    if not _verify_signature(raw, sig):
        return jsonify({"ok": False, "error": "bad_signature"}), 400

    payload = request.get_json(silent=True) or {}
    event = payload.get("meta", {}).get("event_name", "")
    attrs = (payload.get("data", {}) or {}).get("attributes", {}) or {}

    email = (attrs.get("user_email") or attrs.get("email") or "").strip().lower()
    name  = (attrs.get("user_name") or "").strip()

    success_events = {"subscription_created", "subscription_payment_success", "order_created"}

    if email and event in success_events:
        # TODO: burada hesabı PRO yap (kendi fonksiyonunla):
        # set_user_pro_by_email(email)
        try:
            send_pro_activated_email(email, name)
        except Exception as e:
            print("Pro mail send failed:", e)

    return jsonify({"ok": True})
