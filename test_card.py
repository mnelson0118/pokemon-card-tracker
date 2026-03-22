"""
test_card.py
------------
Pulls a single card from the JustTCG API and prints everything returned.
Usage: python test_card.py
"""

import json
import requests

# ── Config ────────────────────────────────────────────────────────────────────

API_KEY = "tcg_32485d5005e746dc87d38149471c3260"   # ← paste your key here
print(f"Using key: {API_KEY[:8]}...")
PRODUCT_ID = "84032"               # ← Bulbasaur (Crystal Guardians), change to any productId


# ── Fetch ─────────────────────────────────────────────────────────────────────

url = "https://api.justtcg.com/v1/cards"
headers = {"x-api-key": API_KEY}
params = {"tcgplayerId": PRODUCT_ID}

response = requests.get(url, headers=headers, params=params, timeout=10)

print(f"Status: {response.status_code}")
print(f"URL: {response.url}")
print()

if response.ok:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print("Error:", response.text)