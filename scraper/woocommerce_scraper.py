import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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

                # Fallback: fetch price from detail page if missing
                final_price = "N/A"
                if price:
                    final_price = price.get_text(strip=True)
                else:
                    try:
                        detail_response = requests.get(product_url, headers=headers, timeout=10)
                        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                        detail_price = (
                            detail_soup.select_one('.price') or
                            detail_soup.select_one('p.price') or
                            detail_soup.select_one('span.woocommerce-Price-amount')
                        )
                        if detail_price:
                            final_price = detail_price.get_text(strip=True)
                    except:
                        pass

                # Optional: check if Out of Stock (from listing page)
                stock = product.select_one('.stock')
                stock_text = stock.get_text(strip=True) if stock else ""

                product_data.append({
                    "title": title.get_text(strip=True),
                    "price": final_price,
                    "description": "",  # Optional
                    "stock": stock_text,
                    "image": urljoin(url, img_url),
                    "url": product_url
                })

        return product_data if product_data else "No products found on the page."

    except Exception as e:
        return {"error": str(e)}
