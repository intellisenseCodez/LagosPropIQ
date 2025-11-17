import json                                                             # to load my data as json
import os                                                               # tto create folders
import time
from datetime import datetime
from functions import scrape_items_from_page, scrape_detail_page

# === LIBRARY TO INCREASES MY SCRAPER SPEED ===
from concurrent.futures import ThreadPoolExecutor

# === SETTING UP MY FILE PATH TO SAVE MY WORK USING THE CURRENT TIME TO UNIQUELY KNOW THE DATE MY DATA WAS SCRAPED ===
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# === BASE URL FOR THE MAIN PAGE ===
URLS = {
    "sale": "https://jiji.ng/lagos/houses-apartments-for-sale",
    "rent": "https://jiji.ng/lagos/houses-apartments-for-rent"
}

# === MY SCRAPING CONFIGURATION  DETAILS===
TARGET_PER_TYPE = 3000          # how many properties to scrape per category (rent/sale)
DELAY_PAGE      = 0.7           # seconds to wait between pages 
MAX_CONCURRENT  = 6             # speeds up how many detail pages I scrape at the same time 


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
        print(f" [Page {page}] {url}")

        items = scrape_items_from_page(url)
        if not items:
            print(" No more items. Stopping...")
            break

        new = 0

        # === COLLECT ALL VALID LISTING URLs FIRST SO I CAN BLAST THEM CONCURRENTLY ===
        detail_urls_with_card = []
        for item in items:
            if len(all_properties) >= target:
                break
            detail_url = item.get("listing_url")
            if not detail_url or detail_url in seen_urls or not detail_url.startswith("https://jiji.ng"):
                continue
            seen_urls.add(detail_url)
            detail_urls_with_card.append((detail_url, item))

        # === IF I HAVE NEW URLs → SCRAPE THEM ALL AT ONCE (ROCKET MODE) ===
        if detail_urls_with_card:
            print(f" → Scraping {len(detail_urls_with_card)} detail pages at once (max {MAX_CONCURRENT})...")
            with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
                results = executor.map(
                    lambda x: {**x[1], **scrape_detail_page(x[0]), "source": "jiji", "listing_type": category},
                    detail_urls_with_card
                )
                for full_item in results:
                    if len(all_properties) >= target:
                        break
                    all_properties.append(full_item)
                    new += 1

                    # === LIVE SAVE EVERY 2000 PROPERTIES  ===
                    if len(all_properties) % 2000 == 0 and all_properties:
                        live_filename = os.path.join(RAW_DIR, f"jiji_{category}_live_{int(time.time())}.json")
                        try:
                            with open(live_filename, 'w', encoding='utf-8') as f:
                                json.dump(all_properties, f, indent=2, ensure_ascii=False)
                            print(f" LIVE SAVE → {len(all_properties)} properties → {live_filename}")
                        except Exception as e:
                            print(f" Live save failed: {e}")
                    # =====================================================

        print(f" Added {new} new properties from page {page}")
        if new == 0 or len(items) < 10:
            print(" No new items. End.")
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
        print(f" {category.upper()}: {len(data)} scraped")

    # === FINAL SAVE TO THE RAW DATA FOLDER as "FILEPATH" IN JSON FORMAT ===
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