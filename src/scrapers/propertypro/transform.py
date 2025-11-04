
import re

class Transformer:
    """
    Transformer handles normalization and transformation of scraped data
    to maintain consistency before insertion into the database.
    """

    @staticmethod
    def clean_price(price_str: str):
        """
        Extracts numeric values from price strings and converts to float.
        Example: "₦2,500,000" -> 2500000.0
        """
        if not price_str:
            return None

        # Remove currency symbols and non-numeric characters
        price_str = re.sub(r"[^\d.]", "", price_str)
        try:
            return float(price_str)
        except ValueError:
            return None
        
    @staticmethod
    def normalize_location(location_str: str):
        """
        Cleans and formats location strings to title case.
        Example: "lekki phase 1, lagos" -> "Lekki Phase 1, Lagos"
        """
        if not location_str:
            return None
        return location_str.strip().title()
    
    @staticmethod
    def normalize_text(text: str):
        """
        Removes excessive whitespace and standardizes casing for general text.
        Example: "  Spacious 4 Bedroom  " -> "Spacious 4 Bedroom"
        """
        if not text:
            return None
        return re.sub(r"\s+", " ", text.strip())
    
    @staticmethod
    def clean_bedrooms(bedroom_str: str):
        """
        Extracts numeric bedroom values from strings.
        Example: "3 Bedrooms" -> 3
        """
        if not bedroom_str:
            return None
        match = re.search(r"\d+", bedroom_str)
        return int(match.group()) if match else None

    @staticmethod
    def clean_bathrooms(bathroom_str: str):
        """
        Extracts numeric bathroom values from strings.
        Example: "2 Bathrooms" -> 2
        """
        if not bathroom_str:
            return None
        match = re.search(r"\d+", bathroom_str)
        return int(match.group()) if match else None