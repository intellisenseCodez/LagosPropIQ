import requests
from bs4 import BeautifulSoup

def make_request(url: str):
    """I make a GET request to the given URL and return the response object."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            print("Response Not Available")
            return None
    except Exception as e:
        print("I could not access the resource:", e)
        return None


def parse_page(html_content):
    """I convert raw HTML content into a BeautifulSoup object."""
    return BeautifulSoup(html_content, "html.parser")


def extract_container(soup):
    """I find the main product container div."""
    return soup.find("div", class_="masonry-wall b-list-advert__gallery")


def extract_all_items(container):
    """I extract all individual product masonry items."""
    return container.find_all("div", class_="masonry-item")


def scrape_items_from_page(all_product_mansory):
    """
    # I use a loop to get all PRODUCT ITEMS FOR THE BASE URL
    """
    all_items_per_page = []
    for product_items in all_product_mansory:
        title = product_items.find("div", class_="b-list-advert-base__data__title").text
        prop_price = product_items.find("div", class_="b-list-advert-base__data__price").text
        prop_description = product_items.find("div", class_="b-list-advert-base__description").text
        prop_location = product_items.find("span", class_="b-list-advert__region__text").text
        prop_size_sqm = product_items.find("div", class_="b-list-advert-base__item-attr").text
       
        all_product_mansory_items = {
            "property_title": title,
            "price": prop_price,
            "description": prop_description,
            "location": prop_location,
            "size_sqm": prop_size_sqm
        }
        all_items_per_page.append(all_product_mansory_items)
    return all_items_per_page