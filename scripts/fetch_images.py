"""
fetch_images.py
---------------
Reads pokemon-data.csv and:
1. Fills in any missing imageUrl values using the TCGPlayer CDN pattern
2. Fetches market prices from JustTCG API by card name
   - Writes results to the marketPrice column nightly

The [skip ci] tag on the commit message prevents an infinite trigger loop.
"""

import csv
import os
import re
import sys
import time
from pathlib import Path

import requests

# ── Config ────────────────────────────────────────────────────────────────────

CSV_PATH = Path("pokemon-data.csv")
CDN_PATTERN = "https://tcgplayer-cdn.tcgplayer.com/product/{product_id}_in_1000x1000.jpg"
JUSTTCG_API_KEY = os.environ.get("JUSTTCG_API_KEY", "")
JUSTTCG_BASE_URL = "https://api.justtcg.com/v1/cards"
REQUEST_DELAY = 0.5
REQUEST_TIMEOUT = 10

HEADERS = {
    "Authorization": f"Bearer {JUSTTCG_API_KEY}",
    "Content-Type": "application/json"
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_product_id_from_url(url: str):
    match = re.search(r"/product/(\d+)/", url)
    return match.group(1) if match else None


def fallback_image_url(row: dict):
    product_id = (row.get("productId") or "").strip()
    if not product_id:
        product_id = extract_product_id_from_url(row.get("cardLink") or "")
    if product_id:
        return CDN_PATTERN.format(product_id=product_id)
    return ""


def fetch_market_price(card_name: str):
    """
    Search JustTCG for the card by name and return the market price.
    Returns None if not found or on error.
    """
    if not JUSTTCG_API_KEY:
        print("  ⚠️  JUSTTCG_API_KEY not set", file=sys.stderr)
        return None

    try:
        response = requests.get(
            JUSTTCG_BASE_URL,
            headers=HEADERS,
            params={"q": card_name, "game": "pokemon"},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()

        cards = data.get("data", [])
        if not cards:
            return None

        # Find best match — prefer exact name match
        for card in cards:
            if card.get("name", "").lower() == card_name.lower():
                price = extract_price(card)
                if price:
                    return price

        # Fall back to first result
        return extract_price(cards[0])

    except requests.RequestException as exc:
        print(f"  ⚠️  API error ({exc.__class__.__name__})", file=sys.stderr)
        return None


def extract_price(card: dict):
    """Pull market price from a JustTCG card object."""
    prices = card.get("prices", {})

    # Try near mint market price first
    for condition in ["near_mint", "lightly_played"]:
        condition_data = prices.get(condition, {})
        market = condition_data.get("market_price") or condition_data.get("mid_price")
        if market:
            return float(market)

    # Fallback: any price we can find
    for condition_data in prices.values():
        if isinstance(condition_data, dict):
            for key in ["market_price", "mid_price", "low_price"]:
                if condition_data.get(key):
                    return float(condition_data[key])

    return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not JUSTTCG_API_KEY:
        print("❌ JUSTTCG_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    if not CSV_PATH.exists():
        print(f"❌ CSV not found: {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("CSV is empty — nothing to do.")
        return

    fieldnames = list(rows[0].keys())

    if "imageUrl" not in fieldnames:
        fieldnames.append("imageUrl")
    if "marketPrice" not in fieldnames:
        fieldnames.append("marketPrice")

    # Step 1: Fill missing imageUrls
    image_updated = 0
    for row in rows:
        if not (row.get("imageUrl") or "").strip():
            image_url = fallback_image_url(row)
            if image_url:
                row["imageUrl"] = image_url
                image_updated += 1
    print(f"✅ ImageUrl: updated {image_updated} missing rows")

    # Step 2: Fetch market prices from JustTCG
    print(f"\n🔍 Fetching market prices for {len(rows)} cards from JustTCG...")
    price_updated = 0
    price_failed = 0

    for i, row in enumerate(rows):
        name = (row.get("name") or "").strip()

        if not name:
            price_failed += 1
            continue

        print(f"  [{i+1}/{len(rows)}] {name} ...", end=" ", flush=True)

        price = fetch_market_price(name)

        if price is not None:
            row["marketPrice"] = round(price, 2)
            price_updated += 1
            print(f"${price:.2f} ✅")
        else:
            row["marketPrice"] = row.get("marketPrice", "")
            price_failed += 1
            print(f"not found ⚠️")

        time.sleep(REQUEST_DELAY)

    # Write back
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Done! Prices updated: {price_updated}, failed: {price_failed}")
    print(f"✅ Saved {CSV_PATH}")


if __name__ == "__main__":
    main()
