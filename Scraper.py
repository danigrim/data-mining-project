import requests
from bs4 import BeautifulSoup
from selenium import webdriver

URL='https://techcrunch.com/'

class Scraper:
    def __init__(self, url):
        self.page = requests.get(url)
        if self.page.status_code == requests.codes.ok:
            print("URL Fetching succesful...\n")
        else:
            raise Exception("Issue with get request to url")

    def scrape(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        # divs = soup.find_all(class_='mini-view')
        # print(divs)
        # for div in divs:
        #     articles = div.findChildren("article", recursive=True)
        #     for a in articles:
        #         h3 = a.findChildren("h3", recursive=True)
        #         for h in h3:
        #             links = h.findChildren("a", recursive=True)
        #             for link in links:
        #                 link['href']

        article_titles = soup.find_all(href=True, class_="post-block__title__link")
        # get all titles
        articles = set()
        for title in article_titles:
           articles.add(title['href'])
        print(articles)



        #article_links = article_divs.find(href = True)

       # print()
        #links = soup.find_all('article', )
       # print(links)
        #pages = [a.find('a')['href'] for a in links if a != '']
        #print(pages)


if __name__ == '__main__':
    tcScraper = Scraper(URL)
    tcScraper.scrape()