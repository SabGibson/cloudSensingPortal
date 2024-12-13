from bs4 import BeautifulSoup
import logging
import json
import re

def extract_product_info(html_content):
    """
    Extract product information from Amazon HTML content.
    Returns a list of dictionaries containing product details.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    
    # Find all product cards
    product_cards = soup.find_all('li', class_='a-carousel-card')
    
    for card in product_cards:
        product_info = {}
        
        # Find the product div inside the carousel card
        product_div = card.find('div', class_='p13n-sc-uncoverable-faceout')
        if not product_div:
            continue
        
        # Extract product title
        title_elem = product_div.find('div', class_='p13n-sc-truncate-desktop-type2')
        if title_elem:
            product_info['title'] = title_elem.get('title', '').strip()
        
        # Extract ASIN (Amazon product ID)
        if 'id' in product_div.attrs:
            product_info['asin'] = product_div['id']
        
        # Extract price
        price_elem = product_div.find('span', class_='_cDEzb_p13n-sc-price_3mJ9Z')
        if price_elem:
            price_text = price_elem.text.strip()
            if price_text != "Click for details":
                price = float(re.sub(r'[^\d.]', '', price_text))
                product_info['price'] = price
        
        # Extract review count
        reviews_elem = product_div.find('span', class_='a-size-small')
        if reviews_elem:
            try:
                reviews = int(reviews_elem.text.replace(',', ''))
                product_info['review_count'] = reviews
            except (ValueError, AttributeError):
                pass
        
        if product_info.get('title') and (product_info.get('price') or product_info.get('asin')):
            products.append(product_info)
    
    return products

def format_as_json(products):
    """Format the products list as JSON string"""
    return json.dumps(products, indent=2)

def process_amazonuk_html(html_content):
    logging.info(f"type for output is {type(html_content)}")
    """Process the HTML content and return JSON string"""
    products = extract_product_info(html_content)
    return format_as_json(products)