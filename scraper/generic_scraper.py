from flask import Flask, render_template, request
from scraper.generic_scraper import scrape_generic
from scraper.woocommerce_scraper import scrape_woocommerce
from scraper.sitemap_scraper import scrape_sitemap

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    site_type = None  # Track selected site type
    url = ""

    if request.method == "POST":
        input_url = request.form.get("url", "").strip().lower()
        site_type = request.form.get("site_type")

        # Auto format the URL
        if not input_url.startswith("http://") and not input_url.startswith("https://"):
            if "." not in input_url:
                # Treat as search keyword, build domain
                formatted = input_url.replace(" ", "")
                input_url = f"https://{formatted}.com"
            else:
                input_url = f"https://{input_url}"

        url = input_url

        try:
            if site_type == "generic":
                result = scrape_generic(url)
            elif site_type == "woocommerce":
                result = scrape_woocommerce(url)
            elif site_type == "sitemap":
                result = scrape_sitemap(url)
            else:
                result = "Invalid site type selected."
        except Exception as e:
            result = f"Error scraping: {str(e)}"

    return render_template("index.html", result=result, site_type=site_type)

if __name__ == "__main__":
    app.run(debug=True)
