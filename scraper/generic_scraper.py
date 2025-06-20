import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_generic(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Title
        title = soup.title.string.strip() if soup.title else 'No Title Found'

        # Extract Headings
        headings = {
            "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
            "h2": [h.get_text(strip=True) for h in soup.find_all("h2")],
            "h3": [h.get_text(strip=True) for h in soup.find_all("h3")],
        }

        # Extract first 5 paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")[:5]]

        # Extract internal and external links
        links = []
        for a in soup.find_all("a", href=True):
            link_text = a.get_text(strip=True)
            full_url = urljoin(url, a['href'])
            links.append({"text": link_text, "url": full_url})

        return {
            "title": title,
            "headings": headings,
            "paragraphs": paragraphs,
            "links": links[:10]  # limit to 10 for brevity
        }

    except Exception as e:
        return {"error": str(e)}
