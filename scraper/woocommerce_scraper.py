import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_woocommerce(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_data = []

        product_blocks = soup.select('.product')  # Most WooCommerce themes use this class

        for product in product_blocks:
            title_tag = product.select_one('.woocommerce-loop-product__title')
            price_tag = product.select_one('.price')
            img_tag = product.select_one('img')
            link_tag = product.select_one('a')

            if title_tag and img_tag and link_tag:
                product_data.append({
                    "title": title_tag.get_text(strip=True),
                    "price": price_tag.get_text(strip=True) if price_tag else "N/A",
                    "description": "",  # Empty for now — needs product detail page
                    "image": img_tag['src'],
                    "url": urljoin(url, link_tag['href']),
                })

        return product_data or "No products found on the page."

    except Exception as e:
        return {"error": str(e)}
