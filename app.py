from flask import Flask, render_template, request
from scraper.generic_scraper import scrape_generic
from scraper.woocommerce_scraper import scrape_woocommerce
from scraper.sitemap_scraper import scrape_sitemap

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    site_type = None  # Track selected site type

    if request.method == "POST":
        input_url = request.form.get("url").strip().lower()
        site_type = request.form.get("site_type")

        # ✅ Step 1: Format raw inputs
        if not input_url.startswith("http://") and not input_url.startswith("https://"):
            if "." not in input_url:
                input_url = f"https://{input_url}.com"
            else:
                input_url = f"https://{input_url}"

        url = input_url

        # ✅ Step 2: Call scraper based on site_type
        if site_type == "generic":
            result = scrape_generic(url)
        elif site_type == "woocommerce":
            result = scrape_woocommerce(url)
        elif site_type == "sitemap":
            result = scrape_sitemap(url)

    return render_template("index.html", result=result, site_type=site_type)

if __name__ == "__main__":
    app.run(debug=True)
