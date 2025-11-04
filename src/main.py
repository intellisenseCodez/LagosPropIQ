import os
from pathlib import Path
import time
from src.scrapers.propertypro.etl import PropertyProScraper
from src.utils import loader

RAW_DIR = Path("src/data/raw")
TRANSFORM_DIR = Path("src/data/transform")


RAW_DIR.mkdir(parents=True, exist_ok=True)
TRANSFORM_DIR.mkdir(parents=True, exist_ok=True)


propetypro_scraper = PropertyProScraper()

# extract
for property in propetypro_scraper.extract(pages=2):
    # load raw
    loader.to_csv(property, filename=RAW_DIR / "property.csv")



