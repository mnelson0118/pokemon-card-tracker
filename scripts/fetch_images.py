"""
fetch_images.py
---------------
Reads pokemon-data.csv and:
1. Fills in any missing imageUrl values using the TCGPlayer CDN pattern
2. Scrapes the market price from each card's TCGPlayer page nightly

Only imageUrl rows that are blank are updated.
Market prices are always refreshed on every run.
The [skip ci] tag on the commit message prevents an infinite trigger loop.
"""

import csv
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Config ────────────────────────────────────────────────────────────────────

CSV_PATH = Path("pokemon-data.csv")

CDN_PATTERN = "https://tcgplayer-cdn.tcgplayer.com/product/{product_id}_in_1000x1000.jpg"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

REQUEST_DELAY = 1.5   # seconds between requests
REQUEST_TIMEOUT = 10  # seconds


# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_product_id_from_url(url: str):
    """Pull the numeric productId out of a TCGPlayer URL path segment."""
    match = re.search(r"/product/(\d+)/", url)
    return match.group(1) if match else None


def fallback_image_url(row: dict):
    """Build CDN URL from productId column, or from cardLink if column is empty."""
    product_id = (row.get("productId") or "").strip()
    if not product_id:
        product_id = extract_product_id_from_url(row.get("cardLink") or "")
    if product_id:
        return CDN_PATTERN.format(product_id=product_id)
    return ""


def scrape_market_price(card_link: str):
    """
    Fetch the cardLink page and return the market price as a float.
    Returns None on any error or if price not found.
    """
    try:
        response = requests.get(card_link, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"  ⚠️  Request failed ({exc.__class__.__name__})", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Try to find the market price span
    price_span = soup.find("span", class_="price-points__upper__price")
    if price_span:
        price_text = price_span.get_text(strip=True).replace("$", "").replace(",", "")
        try:
            return float(price_text)
        except ValueError:
            pass

    # Fallback: look for any element containing market price
    for tag in soup.find_all(string=re.compile(r"Market Price", re.I)):
        parent = tag.parent
        if parent:
            sibling = parent.find_next(string=re.compile(r"\$[\d,.]+"))
            if sibling:
                price_text = sibling.strip().replace("$", "").replace(",", "")
                try:
                    return float(price_text)
                except ValueError:
                    pass

    return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not CSV_PATH.exists():
        print(f"❌ CSV not found: {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("CSV is empty — nothing to do.")
        return

    fieldnames = list(rows[0].keys())

    # Ensure imageUrl and marketPrice columns exist
    if "imageUrl" not in fieldnames:
        fieldnames.append("imageUrl")
    if "marketPrice" not in fieldnames:
        fieldnames.append("marketPrice")

    # Step 1: Fill missing imageUrls (fast, no requests)
    image_updated = 0
    for row in rows:
        if not (row.get("imageUrl") or "").strip():
            image_url = fallback_image_url(row)
            if image_url:
                row["imageUrl"] = image_url
                image_updated += 1
    print(f"✅ ImageUrl: updated {image_updated} missing rows")

    # Step 2: Scrape market prices for all rows
    print(f"\n🔍 Scraping market prices for {len(rows)} cards...")
    price_updated = 0
    price_failed = 0

    for i, row in enumerate(rows):
        card_link = (row.get("cardLink") or "").strip()
        name = row.get("name", row.get("id", "?"))

        if not card_link:
            print(f"  ⏭️  Skipping '{name}' — no cardLink")
            price_failed += 1
            continue

        print(f"  [{i+1}/{len(rows)}] {name} ...", end=" ", flush=True)

        price = scrape_market_price(card_link)

        if price is not None:
            row["marketPrice"] = price
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
