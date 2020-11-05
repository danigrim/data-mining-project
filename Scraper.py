import requests
from bs4 import BeautifulSoup

URL = 'https://techcrunch.com/


class Scraper:
    def __init__(self, url):
        self.page = requests.get(url)
        if self.page.status_code == requests.codes.ok:
            print("URL Fetching successful...\n")
        else:
            raise Exception("Issue with get request to url")

    def scrape(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')

        article_titles = soup.find_all(href=True, class_="post-block__title__link")
        # get all titles
        articles = set()
        for title in article_titles:
            articles.add(title['href'])
        print(articles)


