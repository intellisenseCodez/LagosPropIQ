import json   # to load my data as json
import os
import time
from datetime import datetime
from functions import scrape_items_from_page, scrape_detail_page

# === SETTING UP MY FILE PATH TO SAVE MY WORK USING THE CURRENT TIME TO UNIQUELY KNOW THE DATE MY DATA WAS SCRAPED ===
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# === BASE URL FOR THE MAIN PAGE ===
URLS = {
    "sale": "https://jiji.ng/lagos/houses-apartments-for-sale",
    "rent": "https://jiji.ng/lagos/houses-apartments-for-rent"
}

# === SCRAPING CONFIGURATION ===
TARGET_PER_TYPE = 3000        # how many properties to scrape per category (rent/sale)
DELAY_PAGE = 1.5                # seconds to wait between pages
DELAY_ITEM = 0.8              # seconds to wait between detail pages


def scrape_category(category: str, base_url: str):
    """Scrape one category (rent or sale) up to TARGET_PER_TYPE properties"""
    print(f"\nSTARTING {category.upper()} SCRAPER → Target: {TARGET_PER_TYPE}")
    all_properties = []
    page = 1
    seen_urls = set()

    # === SET TARGET AND BASE URL FOR THIS CATEGORY ===
    target = TARGET_PER_TYPE
    BASE_URL = base_url

    while len(all_properties) < target:
        url = f"{BASE_URL}?page={page}"
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

            # === MERGE LISTING CARD + DETAIL PAGE DATA I SCRAPED WITH THE DETAIL URL TO MAKE ONE COMPLETE PROPERTY ===
            full_item = {**item, **detail, "source": "jiji", "listing_type": category}
            all_properties.append(full_item)
            new += 1

            # === LIVE SAVE EVERY 2000 PROPERTIES JUST IN CASE ===
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
            print("  No new items. End.")
            break

        page += 1
        time.sleep(DELAY_PAGE)

    return all_properties[:target]


def main():
    """Main function to run both rent and sale scrapers"""
    print("STARTING FULL LAGOS PROPERTY SCRAPER (SALE + RENT)")
    results = {}

    for category, base_url in URLS.items():
        print(f"\n{'='*60}")
        data = scrape_category(category, base_url)
        results[category] = data
        print(f"  {category.upper()}: {len(data)} scraped")

     # === FINAL SAVE TO THE RAW DATA FOLDER IN JSON FORMAT ===
    for category, data in results.items():
        if not data:
            continue
        filename = f"lagos_{category}_raw_{TIMESTAMP}.json"
        filepath = os.path.join(RAW_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f" SAVED → {filepath}")
        
# === JUST A PRINT STATEMENT TO SHOW THE NUMBER OF SUCCESSFULLY SCRAPED PROPERTIES I DID ===
    total = sum(len(v) for v in results.values())
    print(f"\nSUCCESS! Total: {total} properties scraped.")


# === STARTING POINT OF MY CODE ===
if __name__ == "__main__":
    main()