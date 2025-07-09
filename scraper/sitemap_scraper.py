import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_sitemap(url):
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

        links = set()

        if url.endswith(".xml"):
            soup = BeautifulSoup(response.content, "xml")
            for loc in soup.find_all("loc"):
                link = loc.text.strip()
                if link:
                    links.add(link)
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a['href'].strip()
                if href:
                    full_url = urljoin(url, href)
                    links.add(full_url)

        return {
            "title": f"Sitemap Links from {urlparse(url).netloc}",
            "headings": {},
            "paragraphs": [],
            "links": [{"url": link, "text": link} for link in sorted(links)],
            "images": []
        }

    except Exception as e:
        return {
            "error": f"Failed to parse sitemap from {url}: {str(e)}"
        }
