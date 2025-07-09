import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
<<<<<<< HEAD

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
=======
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_detail_price(product_url, headers):
    try:
        detail_response = requests.get(product_url, headers=headers, timeout=10)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        detail_price = (
            detail_soup.select_one('.price') or
            detail_soup.select_one('p.price') or
            detail_soup.select_one('span.woocommerce-Price-amount')
        )
        return detail_price.get_text(strip=True) if detail_price else "N/A"
    except:
        return "N/A"

def scrape_woocommerce(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_data = []
        product_blocks = (
            soup.select('ul.products li.product') or
            soup.select('.woocommerce ul.products li') or
            soup.select('div.products .product') or
            soup.select('.product')
        )

        tasks = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for product in product_blocks:
                title = product.select_one('.woocommerce-loop-product__title') or product.select_one('h2')
                price = product.select_one('.price')
                link = product.select_one('a')
                img = product.select_one('img')

                if title and link and img:
                    img_url = (
                        img.get('data-src') or
                        img.get('data-lazy-src') or
                        img.get('src') or
                        ""
                    )
                    product_url = urljoin(url, link['href'])

                    if price:
                        final_price = price.get_text(strip=True)
                        product_data.append({
                            "title": title.get_text(strip=True),
                            "price": final_price,
                            "description": "",
                            "image": urljoin(url, img_url),
                            "url": product_url
                        })
                    else:
                        # Schedule detail page fetch
                        tasks.append({
                            "title": title.get_text(strip=True),
                            "image": urljoin(url, img_url),
                            "url": product_url,
                            "future": executor.submit(fetch_detail_price, product_url, headers)
                        })

            # Add fetched detail prices
            for task in tasks:
                price = task["future"].result()
                product_data.append({
                    "title": task["title"],
                    "price": price,
                    "description": "",
                    "image": task["image"],
                    "url": task["url"]
                })

        return product_data if product_data else "No products found on the page."
>>>>>>> 89f51f3 (Updated scraper code from new system)

    except Exception as e:
        return {"error": str(e)}
