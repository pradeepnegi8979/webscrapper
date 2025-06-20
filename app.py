from flask import Flask, render_template, request
from scraper.generic_scraper import scrape_generic
from scraper.woocommerce_scraper import scrape_woocommerce

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        site_type = request.form.get("site_type")

        if site_type == "generic":
            result = scrape_generic(url)
        elif site_type == "woocommerce":
            result = scrape_woocommerce(url)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
