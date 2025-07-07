# ===================== wallet/utils/paystack.py =====================
import requests
from django.conf import settings

PAYSTACK_INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"
PAYSTACK_CHARGE_URL = "https://api.paystack.co/transaction/charge_authorization"

HEADERS = {
    "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    "Content-Type": "application/json"
}

def initialize_transaction(email, amount):
    data = {
        "email": email,
        "amount": amount,
        "channels": ["bank"],
        "metadata": {
            "custom_filters": {
                "recurring": True
            }
        }
    }
    response = requests.post(PAYSTACK_INITIALIZE_URL, json=data, headers=HEADERS)
    return response.json()

def charge_authorization(email, amount, authorization_code):
    data = {
        "email": email,
        "amount": amount,
        "authorization_code": authorization_code
    }
    response = requests.post(PAYSTACK_CHARGE_URL, json=data, headers=HEADERS)
    return response.json()
