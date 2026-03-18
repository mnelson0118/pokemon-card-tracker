#!/usr/bin/env python3
"""
Fetch real product images from TCGPlayer CDN and update pokemon-data.csv
with actual imageUrl values
"""

import csv
import requests
from urllib.parse import urljoin
import time
import json

# TCGPlayer CDN pattern - this is what we'll test
TCGPLAYER_CDN_PATTERN = "https://tcgplayer-cdn.tcgplayer.com/product/{productId}_in_1000x1000.jpg"

def check_image_exists(url):
    """Check if an image URL actually exists"""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def fetch_image_for_product(productId):
    """
    Try to fetch image URL for a productId
    Returns the URL if it exists, None otherwise
    """
    if not productId or productId.strip() == '':
        return None
    
    productId = productId.strip()
    
    # Try TCGPlayer CDN URL
    cdn_url = TCGPLAYER_CDN_PATTERN.format(productId=productId)
    
    print(f"  Checking {productId}...", end=" ")
    
    if check_image_exists(cdn_url):
        print(f"✅ Found")
        return cdn_url
    else:
        print(f"❌ Not found")
        return None

def main():
    csv_path = '/mnt/user-data/outputs/pokemon-data.csv'
    
    print("=" * 80)
    print("TCGPLAYER IMAGE URL FETCHER")
    print("=" * 80)
    print()
    
    # Read the CSV
    print(f"📖 Reading {csv_path}...")
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"✅ Loaded {len(rows)} Pokemon\n")
    
    # Process each row
    updated_count = 0
    found_count = 0
    
    print("🖼️  Fetching images from TCGPlayer CDN...")
    print()
    
    for i, row in enumerate(rows, 1):
        name = row.get('name', 'Unknown')
        productId = row.get('productId', '')
        current_imageUrl = row.get('imageUrl', '')
        
        # Skip if already has a valid image URL
        if current_imageUrl and current_imageUrl.strip():
            print(f"[{i}/{len(rows)}] {name:20} - Already has imageUrl ✓")
            found_count += 1
            continue
        
        # Try to fetch image for this product
        image_url = fetch_image_for_product(productId)
        
        if image_url:
            row['imageUrl'] = image_url
            updated_count += 1
            found_count += 1
            print(f"[{i}/{len(rows)}] {name:20} - Updated ✨")
        else:
            print(f"[{i}/{len(rows)}] {name:20} - No image found")
        
        # Be nice to the servers - small delay
        time.sleep(0.1)
    
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Total Pokemon: {len(rows)}")
    print(f"With images: {found_count}")
    print(f"Updated: {updated_count}")
    print(f"Missing: {len(rows) - found_count}")
    print()
    
    # Write back to CSV
    if updated_count > 0:
        print(f"💾 Saving updated CSV...")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"✅ Saved {csv_path}")
    else:
        print("ℹ️  No updates needed")
    
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
