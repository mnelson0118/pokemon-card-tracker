"""
fetch_images.py
---------------
Reads pokemon-data.csv, fills in any missing imageUrl values by:
  1. Scraping the og:image meta tag from the cardLink page.
  2. Falling back to the TCGPlayer CDN pattern using productId.

Only rows where imageUrl is blank are processed, so re-runs are cheap.
The [skip ci] tag on the commit message prevents an infinite loop.
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
        "Mozilla/5.0 (compatible; PokemonImageBot/1.0; "
        "+https://github.com)"
    )
}

REQUEST_DELAY = 1.0   # seconds between requests — be polite to TCGPlayer
REQUEST_TIMEOUT = 10  # seconds


# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_product_id_from_url(url: str) -> str | None:
    """Pull the numeric productId out of a TCGPlayer URL path segment."""
    match = re.search(r"/product/(\d+)/", url)
    return match.group(1) if match else None


def fallback_image_url(row: dict) -> str:
    """Build CDN URL from productId column, or from cardLink if column is empty."""
    product_id = row.get("productId", "").strip()
    if not product_id:
        product_id = extract_product_id_from_url(row.get("cardLink", ""))
    if product_id:
        return CDN_PATTERN.format(product_id=product_id)
    return ""


def scrape_image_url(card_link: str) -> str | None:
    """
    Fetch the cardLink page and return the og:image URL.
    Returns None on any error so the caller can fall back gracefully.
    """
    try:
        response = requests.get(card_link, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"  ⚠️  Request failed ({exc.__class__.__name__}): {card_link}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Try og:image first
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        return og_image["content"].strip()

    # Also try twitter:image as a secondary option
    twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
    if twitter_image and twitter_image.get("content"):
        return twitter_image["content"].strip()

    return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not CSV_PATH.exists():
        print(f"❌ CSV not found: {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("CSV is empty — nothing to do.")
        return

    fieldnames = list(rows[0].keys())

    # Ensure imageUrl column exists
    if "imageUrl" not in fieldnames:
        fieldnames.append("imageUrl")

    needs_update = [r for r in rows if not r.get("imageUrl", "").strip()]
    print(f"Rows needing imageUrl: {len(needs_update)} / {len(rows)}")

    updated = 0

    for row in needs_update:
        card_link = row.get("cardLink", "").strip()
        name = row.get("name", row.get("id", "?"))

        if not card_link:
            print(f"  ⏭️  Skipping '{name}' — no cardLink")
            continue

        print(f"  🔍 Fetching image for {name} …", end=" ", flush=True)

        image_url = scrape_image_url(card_link)

        if image_url:
            print(f"scraped ✅")
        else:
            image_url = fallback_image_url(row)
            if image_url:
                print(f"fallback ✅")
            else:
                print(f"no image found ❌")

        row["imageUrl"] = image_url
        updated += 1
        time.sleep(REQUEST_DELAY)

    # Write back only if something changed
    if updated:
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"\n✅ Updated {updated} rows and saved {CSV_PATH}")
    else:
        print("✅ All rows already have imageUrl — no changes written.")


if __name__ == "__main__":
    main()
