import os, requests

BASE_URL = "https://api.lemonsqueezy.com/v1"
API_KEY = os.getenv("LEMON_API_KEY")
STORE_ID = os.getenv("LEMON_STORE_ID")
VARIANT_ID = os.getenv("LEMON_VARIANT_ID")

def create_checkout(email: str) -> str:
    """
    Verilen e-posta adresi için Lemon Squeezy checkout linki oluşturur.
    """
    assert API_KEY and STORE_ID and VARIANT_ID, "LEMON_* environment variables missing"

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
                "store":   {"data": {"type": "stores",   "id": STORE_ID}},
                "variant": {"data": {"type": "variants", "id": VARIANT_ID}},
            }
        }
    }

    response = requests.post(f"{BASE_URL}/checkouts", headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data["data"]["attributes"]["url"]
