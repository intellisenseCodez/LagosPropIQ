
from datetime import datetime
import re

class Transformer:
    """
    Transformer handles normalization and transformation of scraped data
    to maintain consistency before insertion into the database.
    """

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
    def normalize_property_features(text: str) -> dict:
        """
        Extract property features (beds, baths, flats, kitchen, etc.)
        from a text string using regex.
        
        Example:
            "3 Beds 4 Baths 5 flats 7 kitchen"
            
        Returns:
            {'beds': 3, 'baths': 4, 'flats': 5, 'kitchen': 7}
        """
        mapping = {
            'bed': 'bedrooms',
            'bath': 'bathrooms',
            'flat': 'flats',
            'kitchen': 'kitchens'
        }
        
        # Find all number + word pairs (e.g., "3 Beds", "4 Baths")
        matches = re.findall(r"(\d+)\s*([A-Za-z]+)", text)

        # Convert to dictionary (keys lowercase, plural normalized)
        features = {}
        for num, feature in matches:
            key = feature.lower().rstrip('s')
            key = mapping.get(key, key)
            features[key] = int(num)

        return features



    @staticmethod
    def normalize_update_info(text: str) -> dict:
        """
        Transform a text like 'Updated 02 Nov 2025, Added 25 Jun 2025'
        into a dictionary with datetime objects.
        """
        parts = text.split(',')
        data = {}

        for part in parts:
            key, value = part.strip().split(' ', 1)
            label = key.lower().replace(':', '')
            # Extract date portion
            date_str = value.strip().replace(label.capitalize(), '').strip()
            try:
                date_obj = datetime.strptime(value.strip(), "%d %b %Y")
                data[label] = date_obj
            except ValueError:
                # fallback if parsing fails
                data[label] = value.strip()
    
        return data