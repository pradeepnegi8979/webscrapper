import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_generic(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # Page Title
        title = soup.title.string.strip() if soup.title and soup.title.string else ''

        # Headings grouped
        headings = {
            'h1': [h.get_text(strip=True) for h in soup.find_all('h1')],
            'h2': [h.get_text(strip=True) for h in soup.find_all('h2')],
            'h3': [h.get_text(strip=True) for h in soup.find_all('h3')],
        }

        # Paragraphs (only non-empty)
        paragraphs = [
            p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)
        ]

        # Links (with proper full URL and text fallback)
        links = []
        for a in soup.find_all('a', href=True):
            full_url = urljoin(url, a['href'])
            text = a.get_text(strip=True) or full_url
            links.append({'url': full_url, 'text': text})

        # Images (check for base64/svg/data placeholders)
        images = []
        for img in soup.find_all('img'):
            img_url = img.get('src') or img.get('data-src') or img.get('data-srcset')
            if img_url and not img_url.startswith("data:image"):
                img_url = img_url.split()[0]
                full_img_url = urljoin(url, img_url)
                images.append(full_img_url)

        return {
            'title': title,
            'headings': headings,
            'paragraphs': paragraphs,
            'links': links,
            'images': images
        }

    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to fetch {url}: {str(e)}'}
