import requests
import re
import time
from bs4 import BeautifulSoup
from typing import List, Dict
import os

# === REQUESTS ===
def make_request(url: str, retries: int = 3) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.text
            elif response.status_code == 429:
                print(f"Rate limited! Waiting 15s... (attempt {attempt+1})")
                time.sleep(15)
            else:
                print(f"HTTP {response.status_code} on {url}")
        except requests.RequestException as e:
            print(f"Request failed (attempt {attempt+1}): {e}")
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
    return None


# === PARSE HTML ===
def parse_page(html: str) -> BeautifulSoup | None:
    try:
        return BeautifulSoup(html, "html.parser")
    except Exception as e:
        print("Failed to parse HTML:", e)
        return None


# === EXTRACT LISTINGS CONTAINER ===
def extract_container(soup: BeautifulSoup) -> BeautifulSoup | None:
    return soup.find("div", class_="masonry-wall") or soup.find("div", class_=re.compile(r"masonry-wall|b-list-advert"))


# === EXTRACT INDIVIDUAL ITEMS ===
def extract_all_items(container: BeautifulSoup) -> List[BeautifulSoup]:
    return container.find_all("div", class_=re.compile(r"masonry-item|b-list-advert-base"))


# === SCRAPE LISTINGS PAGE ===
def scrape_items_from_page(url: str) -> List[Dict]:
    print(f"  Scraping page: {url}")
    html = make_request(url)
    if not html:
        return []

    soup = parse_page(html)
    if not soup:
        return []

    container = extract_container(soup)
    if not container:
        print("  Could not find container.")
        return []

    items = extract_all_items(container)
    if not items:
        print("  No items found.")
        return []

    results = []
    for item in items:
        try:
            # Title & URL
            title_tag = item.find("div", class_=re.compile(r"title|advert-title"))
            title = title_tag.get_text(strip=True) if title_tag else ""

            link_tag = item.find("a", href=True)
            listing_url = ""
            if link_tag and link_tag.get("href"):
                href = link_tag["href"].strip()
                listing_url = "https://jiji.ng" + href if href.startswith("/") else href

            # Price
            price_tag = item.find("div", class_=re.compile(r"price|advert-price"))
            price_raw = price_tag.get_text(strip=True) if price_tag else ""
            price = ""
            if price_raw:
                lower = price_raw.lower()
                if any(x in lower for x in ["negotiable", "call", "ask", "p.o.a"]):
                    price = "Negotiable"
                else:
                    clean = re.sub(r"[^\d.kmb]", "", price_raw.lower().replace("₦", "").replace(" ", ""))
                    match = re.search(r"[\d.]+", clean)
                    if match:
                        num = float(match.group())
                        if "k" in clean: num *= 1000
                        elif "m" in clean: num *= 1000000
                        elif "b" in clean: num *= 1000000000
                        price = str(int(num))
                    else:
                        price = "Negotiable"
            else:
                price = "Negotiable"

            # Description
            desc = item.find("div", class_=re.compile(r"description|item-desc"))
            description = desc.get_text(strip=True) if desc else ""

            # Location
            loc = item.find("span", class_=re.compile(r"region|location"))
            location = loc.get_text(strip=True) if loc else ""

            # Size (from card)
            size_text = item.get_text()
            size_match = re.search(r"(\d{1,5}(?:,\d{3})*)\s*sqm", size_text, re.I)
            size_sqm = size_match.group(1).replace(",", "") if size_match else ""

            results.append({
                "property_title": title,
                "price": price,
                "description": description,
                "location": location,
                "size_sqm": size_sqm,
                "listing_url": listing_url,
            })
        except Exception as e:
            print(f"  Error in item: {e}")
            continue

    print(f"  Found {len(results)} items.")
    return results


# === SCRAPE DETAIL PAGE (ROBUST) ===
def scrape_detail_page(url: str) -> Dict:
    print(f"    → Detail: {url}")
    html = make_request(url)
    if not html:
        return {}

    soup = parse_page(html)
    if not soup:
        return {}

    data = {}
    try:
        full_text = soup.get_text(separator=" ", strip=True)

        # Title
        title = soup.find("h1") or soup.find("div", class_=re.compile(r"title|header"))
        data["property_title"] = title.get_text(strip=True) if title else ""

        # Price
        price_tag = soup.find(string=re.compile(r"₦")) or soup.find("div", class_=re.compile(r"price"))
        price_text = price_tag.find_parent().get_text() if price_tag and price_tag.find_parent() else ""
        price_clean = re.sub(r"[^\d]", "", price_text.replace("₦", "").replace(",", ""))
        data["price"] = price_clean if price_clean.isdigit() else "Negotiable"

        # Size SQM
        size_match = re.search(r"(\d{1,5}(?:,\d{3})*)\s*sqm", full_text, re.I)
        data["size_sqm"] = size_match.group(1).replace(",", "") if size_match else ""

        # Bedrooms / Bathrooms
        data["bedrooms"] = re.search(r"(\d+)\s*bed", full_text, re.I)
        data["bedrooms"] = data["bedrooms"].group(1) if data["bedrooms"] else ""
        data["bathrooms"] = re.search(r"(\d+)\s*bath", full_text, re.I)
        data["bathrooms"] = data["bathrooms"].group(1) if data["bathrooms"] else ""

        # Furnishing
        furnishing_match = re.search(r"\b(furnished|unfurnished|semi.furnished)\b", full_text, re.I)
        data["furnishing_status"] = furnishing_match.group(1).title() if furnishing_match else ""

        # Location
        loc = soup.find("div", class_=re.compile(r"location|address|region"))
        data["location"] = loc.get_text(strip=True).replace("Location:", "").strip() if loc else ""

        # Agent
        agent_block = soup.find("div", class_=re.compile(r"seller|agent|contact"))
        data["agent_name"] = ""
        data["agent_company"] = ""
        if agent_block:
            name = agent_block.find(string=re.compile(r"Name|Agent", re.I))
            data["agent_name"] = name.find_parent().get_text(strip=True) if name else ""
            comp = agent_block.find("a")
            data["agent_company"] = comp.get_text(strip=True) if comp else ""

        # Contact
        contact = soup.find("a", href=re.compile(r"tel:"))
        data["contact"] = contact["href"].replace("tel:", "").strip() if contact else ""

        # Images
        imgs = soup.find_all("img", src=re.compile(r"jiji\.ng"))
        valid = [img["src"] for img in imgs if "logo" not in img["src"].lower()][:10]
        data["image_links"] = "; ".join(valid)

        # Description
        desc = soup.find("div", class_=re.compile(r"description|details"))
        data["property_description"] = desc.get_text(strip=True, separator=" ") if desc else ""

        # Property Type
        ptype = ""
        text = (data["property_title"] + " " + data["property_description"]).lower()
        types = {
            "duplex": "Duplex", "bungalow": "Bungalow", "flat": "Flat",
            "mini flat": "Mini Flat", "apartment": "Apartment", "self contain": "Self Contain",
            "land": "Land", "mansion": "Mansion", "terrace": "Terrace"
        }
        for k, v in types.items():
            if k in text:
                ptype = v
                break
        data["property_type"] = ptype

        # Dates
        date = soup.find(string=re.compile(r"posted|added", re.I))
        data["listing_date"] = date.strip() if date else ""
        data["last_updated"] = data["listing_date"]

        # Price per sqm
        if data["price"].isdigit() and data["size_sqm"]:
            try:
                data["prize_per_sqm"] = str(round(int(data["price"]) / int(data["size_sqm"]), 2))
            except:
                data["prize_per_sqm"] = ""
        else:
            data["prize_per_sqm"] = ""

        return data

    except Exception as e:
        print(f"    Detail error: {e}")
        return {}