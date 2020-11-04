import requests
from bs4 import BeautifulSoup

URL = 'https://techcrunch.com/extracrunch/market-analysis/'


class Scraper:
    def __init__(self, url):
        self.page = requests.get(url)
        if self.page.status_code == requests.codes.ok:
            print("URL Fetching successful...\n")
        else:
            raise Exception("Issue with get request to url")

    def scrape(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        print(soup.prettify())
        article_titles, article_contents, article_hrefs = [], [], []
        for tag in soup.findAll("div", {"class": "post-block post-block--image post-block--unread"}):
            tag_header = tag.find("a", {"class": "post-block__title__link"})
            tag_content = tag.find("div", {"class": "post-block__content"})

            article_title = tag_header.get_text().strip()
            article_href = tag_header["href"]
            article_content = tag_content.get_text().strip()

            article_titles.append(article_title)
            article_contents.append(article_content)
            article_hrefs.append(article_href)

if __name__ == '__main__':
    tcScraper = Scraper(URL)
    tcScraper.scrape()