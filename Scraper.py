import requests
from bs4 import BeautifulSoup
from selenium import webdriver


URL='http://techcrunch.com'
ARTICLE = 'https://techcrunch.com/2020/11/05/alibaba-passes-ibm-in-cloud-infrastructure-market-with-over-2b-in-revenue/'

class Scraper:
    def __init__(self, url):
        self.page = requests.get(url)
        if self.page.status_code == requests.codes.ok:
            print("URL Fetching successful...\n")
        else:
            raise Exception("Issue with get request to url")

    def scrape(self):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(URL)
        main_pg = driver.page_source
        soup_wd = BeautifulSoup(main_pg, 'html.parser')
        h3s = soup_wd.find_all("h3")
        print(len(h3s))

        soup = BeautifulSoup(self.page.content, 'html.parser')
        article_titles = soup.find_all(href=True, class_="post-block__title__link")
        # # get all titles
        articles = set()
        for a in article_titles:
           articles.add(a['href'])

        self.get_article_info(articles)


    def get_article_info(self, articles):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(ARTICLE)
        menu_items = driver.find_elements_by_class_name('menu__item')
        print(len(menu_items))
        article = driver.page_source
        soup_2 = BeautifulSoup(article, 'html.parser')
        lis = soup_2.find_all('h3')
        print(len(lis))
        driver.close()


            
if __name__ == '__main__':
    tcScraper = Scraper(URL)
    tcScraper.scrape()