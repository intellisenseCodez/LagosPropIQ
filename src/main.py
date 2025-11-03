import os
from pathlib import Path
from src.scrapers.propertypro.etl import PropertyProScraper
from src.utils import loader

RAW_DIR = Path("src/data/raw")
TRANSFORM_DIR = Path("src/data/transform")


RAW_DIR.mkdir(parents=True, exist_ok=True)
TRANSFORM_DIR.mkdir(parents=True, exist_ok=True)

propetypro_scraper = PropertyProScraper(transform=None)


results = propetypro_scraper.scrape_page(page_number=1)
loader.to_csv(results, filename=RAW_DIR / "property.csv")

print(results[0])