from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

class MediumScraper:
    def __init__(self, source_url):
        self.source_url = source_url
        self.root_url = '{}://{}'.format(urlparse(self.source_url).scheme, urlparse(self.source_url).netloc)

    def scrap_trending_articles(self):
        page_data = requests.get(self.source_url).content
        soup = BeautifulSoup(page_data, "html.parser")

        # Find the main container that holds the trending articles
        trending_articles_container = soup.find("div", class_="ew n bc ex ey ez fa fb fc fd fe ff fg fh fi fj fk fl fm")

        trending_articles_data = []
        if trending_articles_container:
            # Find all the links within the container
            trending_articles = trending_articles_container.find_all("a")

            for article in trending_articles:
                article_title = article.get_text()

                # Extract author name
                author_element = article.find_next("Your-Selector-For-Author-Name")
                author_name = author_element.get_text() if author_element else "Author not specified"

                # Filter out empty entries
                if article_title:
                    # Append both article title and author name combined with a dash
                    trending_articles_data.append(f"{article_title} - {author_name}")

        return trending_articles_data

@app.route('/')
def trending_articles():
    medium_url = "https://medium.com/"
    medium_scraper = MediumScraper(medium_url)
    trending_articles = medium_scraper.scrap_trending_articles()
    return render_template('trending_articles.html', trending_articles=trending_articles)

if __name__ == '__main__':
    app.run(debug=True)
