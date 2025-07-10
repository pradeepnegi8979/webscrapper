import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

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

# ✅ Fetch description from detail page
def fetch_description(product_url, headers):
    try:
        detail_response = requests.get(product_url, headers=headers, timeout=10)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        description = (
            detail_soup.select_one('.woocommerce-product-details__short-description') or
            detail_soup.select_one('.product-short-description') or
            detail_soup.select_one('.entry-summary')
        )
        return description.get_text(strip=True) if description else ""
    except:
        return ""

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
                        description = fetch_description(product_url, headers)
                        product_data.append({
                            "title": title.get_text(strip=True),
                            "price": final_price,
                            "description": description,
                            "image": urljoin(url, img_url),
                            "url": product_url
                        })
                    else:
                        # Fallback to background fetching
                        tasks.append({
                            "title": title.get_text(strip=True),
                            "image": urljoin(url, img_url),
                            "url": product_url,
                            "price_future": executor.submit(fetch_detail_price, product_url, headers),
                            "desc_future": executor.submit(fetch_description, product_url, headers)
                        })

            # Collect future results
            for task in tasks:
                price = task["price_future"].result()
                description = task["desc_future"].result()
                product_data.append({
                    "title": task["title"],
                    "price": price,
                    "description": description,
                    "image": task["image"],
                    "url": task["url"]
                })

        return product_data if product_data else "No products found on the page."

    except Exception as e:
        return {"error": str(e)}
