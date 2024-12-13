from bs4 import BeautifulSoup
import json
import re

def extract_product_info(html_content):
    """
    Extract product information from Amazon Japan HTML content.
    Returns a list of dictionaries containing product details.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    
    # Find all carousel cards
    product_cards = soup.find_all('li', class_='a-carousel-card')
    
    for card in product_cards:
        product_info = {}
        
        # Find the product div inside the carousel card
        product_div = card.find('div', attrs={'data-asin': True})
        if not product_div:
            continue
            
        # Extract ASIN
        product_info['asin'] = product_div.get('data-asin', '')
        
        # Extract rank from badge
        rank_elem = card.find('span', class_='zg-bdg-text')
        if rank_elem:
            rank = rank_elem.text.strip('#')
            product_info['rank'] = int(rank)
        
        # Extract product title
        title_elem = card.find('div', class_='p13n-sc-truncate-desktop-type2')
        if title_elem:
            title = title_elem.get('title', '')
            if not title:
                title = title_elem.text.strip()
            product_info['title'] = title
        
        # Extract price
        price_elem = card.find('span', class_='_cDEzb_p13n-sc-price_3mJ9Z')
        if price_elem:
            price_text = price_elem.text.strip()
            try:
                # Remove currency symbol and convert to float
                price = int(re.sub(r'[^\d]', '', price_text))
                product_info['price'] = price
                product_info['currency'] = '¥'
            except ValueError:
                pass
        
        # Extract rating
        rating_elem = card.find('span', class_='a-icon-alt')
        if rating_elem:
            try:
                rating_text = rating_elem.text.split()[0]
                rating = float(rating_text)
                product_info['rating'] = rating
            except (ValueError, IndexError):
                pass

        # Extract review count
        reviews_elem = card.find('span', class_='a-size-small')
        if reviews_elem and reviews_elem.text:
            try:
                reviews = int(reviews_elem.text.replace(',', ''))
                product_info['review_count'] = reviews
            except (ValueError, AttributeError):
                pass
        
        if product_info:
            products.append(product_info)
    
    return products

def format_as_json(products):
    """Format the products list as JSON string"""
    return json.dumps(products, indent=2, ensure_ascii=False)

def process_amazonjp_html(html_content):
    """Process the HTML content and return JSON string"""
    products = extract_product_info(html_content)
    return format_as_json(products)