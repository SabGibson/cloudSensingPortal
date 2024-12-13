from bs4 import BeautifulSoup
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
    product_cards = soup.find_all('div', class_='p13n-sc-uncoverable-faceout')
    
    for card in product_cards:
        product_info = {}
        
        # Extract product title
        title_elem = card.find('div', class_='p13n-sc-truncate-desktop-type2')
        if title_elem:
            product_info['title'] = title_elem.get('title', '').strip()
        
        # Extract ASIN (Amazon product ID)
        if 'id' in card.attrs:
            product_info['asin'] = card['id']
        
        # Extract price
        price_elem = card.find('span', class_='_cDEzb_p13n-sc-price_3mJ9Z')
        if price_elem:
            # Remove currency symbol and convert to float
            price_text = price_elem.text.strip()
            if price_text != "Click for details":
                price = float(re.sub(r'[^\d.]', '', price_text))
                product_info['price'] = price
        
        rating_elem = card.find('i', class_='a-icon-star-small')
        if rating_elem:
            rating_text = rating_elem.find('span', class_='a-icon-alt')
            if rating_text:
                rating = float(rating_text.text.split()[0])
                product_info['rating'] = rating
        
        reviews_elem = card.find('span', class_='a-size-small')
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
    return json.dumps(products, indent=2)

# Function to process the HTML content
def process_amazonus_html(html_content):
    products = extract_product_info(html_content)
    return format_as_json(products)

