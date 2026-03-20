"""
fetch_images.py
---------------
Reads pokemon-data.csv and fills in any missing imageUrl values
using the TCGPlayer CDN pattern derived from productId.

Only rows where imageUrl is blank are processed, so re-runs are cheap.
The [skip ci] tag on the commit message prevents an infinite trigger loop.
"""

import csv
import re
import sys
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CSV_PATH = Path("pokemon-data.csv")

CDN_PATTERN = "https://tcgplayer-cdn.tcgplayer.com/product/{product_id}_in_1000x1000.jpg"


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

    # Ensure imageUrl column exists
    if "imageUrl" not in fieldnames:
        fieldnames.append("imageUrl")

    needs_update = [r for r in rows if not (r.get("imageUrl") or "").strip()]
    print(f"Rows needing imageUrl: {len(needs_update)} / {len(rows)}")

    updated = 0
    for row in rows:
        if not (row.get("imageUrl") or "").strip():
            image_url = fallback_image_url(row)
            if image_url:
                row["imageUrl"] = image_url
                updated += 1
            else:
                print(f"  ⚠️  No productId for {row.get('name', '?')}")

    if updated:
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"✅ Updated {updated} rows and saved {CSV_PATH}")
    else:
        print("✅ All rows already have imageUrl — no changes written.")


if __name__ == "__main__":
    main()
