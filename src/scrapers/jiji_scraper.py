# jiji_scraper.py
from functions import make_request, parse_page, extract_container, extract_all_items, scrape_items_from_page

from pprint import pprint

# I make a request to Jiji Lagos houses for sale
url = "https://jiji.ng/lagos/houses-apartments-for-sale"

print("I am fetching the page...")
response = make_request(url)

if response is None:
    print("I failed to fetch the page. I am exiting.")
else:
    # I convert the response to BeautifulSoup so it’s more readable
    html_soup = parse_page(response.content)

    # I find the container and all items
    product_div_container = extract_container(html_soup)
    
    if product_div_container is None:
        print("I could not find the product container. The page structure may have changed.")
    else:
        all_product_mansory = extract_all_items(product_div_container)
        print(f"I found {len(all_product_mansory)} properties on this page.")
        print("==" * 40)

        # I scrape all items using my updated loop
        all_items_per_page = scrape_items_from_page(all_product_mansory)

        # I display the results
        pprint(all_items_per_page[:3])  # I show the first 3
        print(f"\nI scraped a total of {len(all_items_per_page)} items.")