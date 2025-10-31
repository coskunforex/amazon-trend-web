import os, requests

BASE_URL = "https://api.lemonsqueezy.com/v1"
API_KEY = os.getenv("LEMON_API_KEY")
STORE_ID = os.getenv("LEMON_STORE_ID")
VARIANT_ID = os.getenv("LEMON_VARIANT_ID")

def create_checkout(email: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {"email": email}
            },
            "relationships": {
                "variant": {"data": {"type": "variants", "id": VARIANT_ID}},
            }
        }
    }

    r = requests.post(f"{BASE_URL}/stores/{STORE_ID}/checkouts", headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    d = r.json()
    return d["data"]["attributes"]["url"]
