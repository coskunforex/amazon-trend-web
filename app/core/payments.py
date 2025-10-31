# app/core/payments.py
import os, requests

# --- DIAGNOSTIC HELPERS ---
import requests, os

BASE_URL = "https://api.lemonsqueezy.com/v1"
API_KEY = os.getenv("LEMON_API_KEY")

def _ls_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "X-Api-Version": "2022-11-16",
    }

def ls_get(path: str):
    """Lemon Squeezy API'den bir path getirir (örnek: stores/123 veya variants/456)."""
    r = requests.get(f"{BASE_URL}/{path.lstrip('/')}", headers=_ls_headers(), timeout=20)
    return r.status_code, r.text
# --- END OF DIAGNOSTIC HELPERS ---


BASE_URL = "https://api.lemonsqueezy.com/v1"

API_KEY   = os.getenv("LEMON_API_KEY")
STORE_ID  = os.getenv("LEMON_STORE_ID")
VARIANT_ID= os.getenv("LEMON_VARIANT_ID")

def create_checkout(email: str) -> str:
    assert API_KEY and STORE_ID and VARIANT_ID, "LEMON_* env vars missing"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "X-Api-Version": "2022-11-16",
    }

    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {"email": email}
            },
            "relationships": {
                "store":   {"data": {"type": "stores",   "id": str(STORE_ID)}},
                "variant": {"data": {"type": "variants", "id": str(VARIANT_ID)}},
            }
        }
    }

    r = requests.post(f"{BASE_URL}/checkouts", headers=headers, json=payload, timeout=30)
    # Hata durumunda anlamak için metni de gösterelim
    try:
        r.raise_for_status()
    except Exception:
        raise RuntimeError(f"{r.status_code} error: {r.text}")

    d = r.json()
    return d["data"]["attributes"]["url"]
