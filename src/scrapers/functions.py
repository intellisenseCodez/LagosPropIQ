import requests
import re                               # regular expression to capture unique patterns for the different fields
import time
from bs4 import BeautifulSoup
from typing import List, Dict
import os                               # used to create and save work on a folder

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


# === EXTRACT LISTINGS CONTAINER HOUSING THE WHOLE CARD ===
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
            title = title_tag.get_text(strip=True) if title_tag else "Unknown"

            link_tag = item.find("a", href=True)
            listing_url = ""
            if link_tag and link_tag.get("href"):
                href = link_tag["href"].strip()
                listing_url = "https://jiji.ng" + href if href.startswith("/") else href

            # Price
            price_tag = item.find("div", class_=re.compile(r"price|advert-price"))
            price_raw = price_tag.get_text(strip=True) if price_tag else ""
            price = "Negotiable"
            if price_raw and "negotiable" not in price_raw.lower():
                clean = re.sub(r"[^\d]", "", price_raw.replace("₦", "").replace(",", ""))
                if clean.isdigit():
                    price = clean

            # Description
            desc = item.find("div", class_=re.compile(r"description|item-desc"))
            description = desc.get_text(strip=True) if desc else "Unknown"

            # Location — real area, not just "Lagos"
            loc_tag = item.find("div", class_=re.compile(r"region|location")) or item.find("span", class_=re.compile(r"region|location"))
            location = "Unknown"
            if loc_tag:
                loc_text = loc_tag.get_text(strip=True)
                if loc_text and loc_text.lower() not in ["lagos", "lagos state"]:
                    location = loc_text

            # Size SQM — only real values
            size_match = re.search(r"(\d{2,4})\s*sq\s*m", item.get_text(), re.I)
            if not size_match:
                size_match = re.search(r"(\d{2,4})\s*m²", item.get_text(), re.I)
            size_sqm = size_match.group(1) if size_match else "Unknown"

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


# === FUNCTION USING REGEX TO GET ALL UNIQUE PHONE NUMBERS INCLUDING COUNTRY CODES OR HAVING SPACES MAKING IT EXCEEDS NORMAL PHONE NO. COUNT ===
def extract_hidden_phone(html: str) -> str:
    """Extract phone from Jiji's hidden React state — works 100% in 2025"""
    patterns = [
        r'"phone":"(\+234\d{10})"',
        r'"clickoutPhone":"(\+234\d{10})"',
        r'"userPhone":"(\+234\d{10})"',
        r'"userPhoneHashed":"[^"]*(\+234\d{10})"',
        r'data-phone=["\'](\+234\d{10})["\']',
        r'window\.__INITIAL_STATE__[^}]*"phone":"(\+234[^"]+)"',
        r'"phone":\s*"(\+234[^"]+)"',
        r"\"phone\":\s*\"(\+234[^\"]+)\"",
    ]
    for p in patterns:
        match = re.search(p, html, re.I)
        if match:
            phone = re.sub(r"\D", "", match.group(1))
            if phone.startswith("234"):
                return "+234" + phone[-10:]
            elif phone.startswith("0"):
                return "+234" + phone[1:]
            else:
                return "+234" + phone[-10:]
    return ""


# === FUNCTION TO SCRAPE DETAIL PAGE  PROPERTIES ===
def scrape_detail_page(url: str) -> Dict:
    print(f"    → Detail: {url}")
    html = make_request(url)
    if not html:
        return {}

    soup = parse_page(html)
    if not soup:
        return {}

    data = {}
    full_text = soup.get_text(separator=" ", strip=True)
    full_text_lower = full_text.lower()

    try:
        # Title
        title_tag = soup.find("h1")
        data["property_title"] = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Price
        price_tag = soup.find("div", class_=re.compile(r"price"))
        price_text = price_tag.get_text(strip=True) if price_tag else ""
        price_clean = re.sub(r"[^\d]", "", price_text.replace("₦", "").replace(",", ""))
        data["price"] = price_clean if price_clean.isdigit() else "Negotiable"

        # Size SQM
        size_match = re.search(r"(\d{2,4})\s*sq\s*m", full_text, re.I)
        if not size_match:
            size_match = re.search(r"(\d{2,4})\s*m²", full_text, re.I)
        data["size_sqm"] = size_match.group(1) if size_match else "Unknown"

        # Bedrooms / Bathrooms
        bed = re.search(r"(\d+)\s*bed", full_text, re.I)
        data["bedrooms"] = bed.group(1) if bed else "Unknown"
        bath = re.search(r"(\d+)\s*bath", full_text, re.I)
        data["bathrooms"] = bath.group(1) if bath else "Unknown"

        # Furnishing
        furnish = re.search(r"\b(furnished|unfurnished|semi.?furnished)\b", full_text_lower)
        data["furnishing_status"] = furnish.group(1).title() if furnish else "Unknown"

        # Location
        loc_div = soup.find("div", class_=re.compile(r"location|address|region"))
        location = "Unknown"
        if loc_div:
            loc_text = loc_div.get_text(strip=True)
            if loc_text and loc_text.lower() not in ["lagos", "lagos state"]:
                location = loc_text.replace("Location:", "").strip()
        data["location"] = location

        # Agent name
        agent_div = soup.find("div", class_=re.compile(r"seller|agent|contact", re.I))
        agent_name = "Unknown"
        if agent_div:
            txt = agent_div.get_text()
            name_match = re.search(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)*", txt)
            if name_match and len(name_match.group(0)) > 2:
                agent_name = name_match.group(0)
        data["agent_name"] = agent_name

        # Contact
        contact = extract_hidden_phone(html)
        if not contact:
            tel = soup.find("a", href=re.compile(r"tel:", re.I))
            if tel and tel.get("href"):
                raw = tel["href"].replace("tel:", "").strip()
                cleaned = re.sub(r"\D", "", raw)
                if len(cleaned) >= 10:
                    contact = "+234" + cleaned[-10:]
        data["contact"] = contact or "Unknown"

        # Images
        imgs = soup.find_all("img", src=re.compile(r"pictures\.jiji\.ng|jiji\.ng"))
        valid = []
        for img in imgs:
            src = img.get("src") or img.get("data-src")
            if src and "logo" not in src.lower() and "avatar" not in src.lower():
                if src.startswith("//"):
                    src = "https:" + src
                valid.append(src)
        if not valid:
            og = soup.find("meta", property="og:image")
            if og and og.get("content"):
                valid.append(og["content"])
        data["image_links"] = "; ".join(valid[:5]) if valid else "Unknown"

        # Description
        desc = soup.find("div", class_=re.compile(r"description|details"))
        data["property_description"] = desc.get_text(strip=True, separator=" ") if desc else "Unknown"

        # Property Type
        ptype = "Unknown"
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

        # Listing date
        date_match = re.search(r"(\d+\s+(second|minute|hour|day|week|month|year)s?\s+ago|just now|yesterday)", full_text_lower)
        data["listing_date"] = date_match.group(1).capitalize() if date_match else "Unknown"
        data["last_updated"] = data["listing_date"]

        # Price per sqm.   DERIVED
        if data["price"].isdigit() and data["size_sqm"] != "Unknown" and data["size_sqm"].isdigit():
            try:
                data["prize_per_sqm"] = str(round(int(data["price"]) / int(data["size_sqm"]), 2))
            except:
                data["prize_per_sqm"] = "Unknown"
        else:
            data["prize_per_sqm"] = "Unknown"

        return data

    except Exception as e:
        print(f"    Detail error: {e}")
        return {}