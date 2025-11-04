from ..base import BaseScraper
from .transform import Transformer
from src.utils.logger import get_logger
from bs4 import BeautifulSoup

import time

class PropertyProScraper(BaseScraper):
    def __init__(self, transform: Transformer):
        super().__init__(base_url="https://www.propertypro.ng/property-for-sale")
        self.transform = transform
        self.logger = get_logger(self.__class__.__name__)
    

    def scrape_page(self, page_number: int):
        """Scrape a single page of listings."""
        url = f"{self.base_url}?page={page_number}"
        html = self.get_html(url)
        if not html:
            return []

        soup = self.parse_html(html)
        
        listings = soup.find_all("div", class_="property-listing-content")
        results = []

        for item in listings:
            try:
                title = item.find('div', class_="pl-title").find("h3").get_text(strip=True) if item.find('div', class_="pl-title").find("h3") is not None else "N/A"
                price = item.find('div', class_="pl-price").find("h3").get_text(strip=True) if item.find('div', class_="pl-price").find("h3") is not None else "N/A"
                location = item.find('div', class_="pl-title").find("p").get_text(strip=True) if item.find('div', class_="pl-title").find("p") is not None else "N/A"
                link = item.find('div', class_="pl-title").find("h6").find('a').get('href') if item.find('div', class_="pl-title").find("h6").find('a') is not None else "N/A"
                agent = item.find("div", class_="flex-grow-1 ms-2").get_text(strip=True) if item.find("div", class_="flex-grow-1 ms-2") is not None else "N/A"
                date = item.find("p", class_="date-added").get_text(strip=True) if item.find("p", class_="date-added") is not None else None
                
                details = item.find('div', class_="pl-price").find("h6").get_text(strip=True) if item.find('div', class_="pl-price").find("h6") is not None else "N/A"
        
                results.append({
                    "title": title,
                    "price": price,
                    "location": location,
                    "link": self.base_url + link,
                    "agent": agent,
                    "date": date,
                    "details": details,
                    "source": "PropertyPro.ng"
                })
            except Exception as e:
                self.logger.warning(f"Error parsing listing: {e}")

        return results
    
    def extract(self, pages: int = 5, delay: float = 2.0):
        all_data = []

        for page in range(1, pages + 1):
            self.logger.info(f"Scraping PropertyPro.ng page {page}...")

            data = self.scrape_page(page)
            all_data.extend(data)

            time.sleep(delay)  
        return all_data
    
    def transform(self):
        pass

    def load(self, db: None):
       pass
