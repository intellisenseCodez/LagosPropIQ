import requests
from bs4 import BeautifulSoup

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_html(self, url):
        """Fetch HTML content with basic error handling."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            return None

    def parse_html(self, html):
        """Convert HTML to BeautifulSoup object."""
        return BeautifulSoup(html, "html.parser")
