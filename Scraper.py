import requests
from bs4 import BeautifulSoup

URL='https://techcrunch.com/extracrunch/market-analysis/'

class Scraper:
    def __init__(self, url):
        self.page = requests.get(url)
        if self.page.status_code == requests.codes.ok:
            print("URL Fetching succesful...\n")
        else:
            raise Exception("Issue with get request to url")

    def scrape(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        print(soup.prettify())


if __name__ == '__main__':
    tcScraper = Scraper(URL)
    tcScraper.scrape()