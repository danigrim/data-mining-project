from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

URL='http://techcrunch.com'

class Scraper:
    def __init__(self, url):
        self.url = url


    def scrape(self):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(self.url)
        articles = set()

        while True:
            curr_articles = set() #this will get current articles to avoid duplicating
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            featured_articles = soup.find_all("h3", class_='mini-view__item__title')
            for a in featured_articles:
                articles.add(a.findChildren('a')[0]['href'])
            latest_articles = soup.find_all(href=True, class_="post-block__title__link")
            # # get all from latest articles
            for a in latest_articles:
                articles.add(a['href'])

            LOAD_MORE_BUTTON_XPATH = '//*[@id="tc-main-content"]/div[2]/div/div/button/span'
            loadMoreButton = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)

            action = ActionChains(driver)
            action.move_to_element(loadMoreButton).click().perform()
            time.sleep(3)
            self.get_article_info(articles)


    def get_article_info(self, articles):
        print(len(articles))
        # driver = webdriver.Chrome('./chromedriver')
        # driver.get(ARTICLE)
        # menu_items = driver.find_elements_by_class_name('menu__item')
        # print(len(menu_items))
        # article = driver.page_source
        # soup_2 = BeautifulSoup(article, 'html.parser')
        # lis = soup_2.find_all('h3')
        # print(len(lis))
        # driver.close()


            
if __name__ == '__main__':
    tcScraper = Scraper(URL)
    tcScraper.scrape()