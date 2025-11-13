import csv
import os
import time
from datetime import datetime
from functions import scrape_items_from_page, scrape_detail_page

# === SETUP ===
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

URLS = {
    "sale": "https://jiji.ng/lagos/houses-apartments-for-sale",
    "rent": "https://jiji.ng/lagos/houses-apartments-for-rent"
}

TARGET_PER_TYPE = 3000
DELAY_PAGE = 3
DELAY_ITEM = 1.5


def scrape_category(category: str, base_url: str, target: int):
    print(f"\nSTARTING {category.upper()} SCRAPER → Target: {target}")
    all_properties = []
    page = 1
    seen_urls = set()

    while len(all_properties) < target:
        url = f"{base_url}?page={page}"
        print(f"  [Page {page}] {url}")

        items = scrape_items_from_page(url)
        if not items:
            print("  No more items. Stopping.")
            break

        new = 0
        for item in items:
            if len(all_properties) >= target:
                break

            detail_url = item.get("listing_url")
            if not detail_url or detail_url in seen_urls or not detail_url.startswith("https://jiji.ng"):
                continue

            seen_urls.add(detail_url)
            print(f"    → {detail_url}")
            detail = scrape_detail_page(detail_url)

            # Merge list + detail data
            full_item = {**item, **detail, "source": "jiji", "listing_type": category}
            all_properties.append(full_item)
            new += 1

            # LIVE SAVE EVERY 2000
            if len(all_properties) % 2000 == 0 and len(all_properties) >= 2000:
                live_file = f"lagos_{category}_partial_{TIMESTAMP}.csv"
                live_path = os.path.join(RAW_DIR, live_file)
                keys = all_properties[0].keys()
                with open(live_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(all_properties)
                print(f"  LIVE SAVE: {len(all_properties)} → {live_path}")

            time.sleep(DELAY_ITEM)

        print(f"  Added {new} new properties from page {page}")
        if new == 0 or len(items) < 10:
            print("  No new items → likely end.")
            break

        page += 1
        time.sleep(DELAY_PAGE)

    return all_properties[:target]


def main():
    print("STARTING FULL LAGOS PROPERTY SCRAPER (SALE + RENT)")
    results = {}

    for category, base_url in URLS.items():
        print(f"\n{'='*60}")
        data = scrape_category(category, base_url, TARGET_PER_TYPE)
        results[category] = data
        print(f"  {category.upper()}: {len(data)} scraped")

    # FINAL SAVE
    for category, data in results.items():
        if not data:
            continue
        keys = data[0].keys()
        filename = f"lagos_{category}_raw_{TIMESTAMP}.csv"
        filepath = os.path.join(RAW_DIR, filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"  SAVED → {filepath}")

    total = sum(len(v) for v in results.values())
    print(f"\nSUCCESS! Total: {total} properties scraped.")


if __name__ == "__main__":
    main()