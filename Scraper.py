from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://techcrunch.com/'


class Scraper:
    def __init__(self, url):
        self.url = url


    def scrape(self):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(self.url)
        articles = set()
        load_button = True
        while load_button:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            featured_articles = soup.find_all("h3", class_='mini-view__item__title')
            for a in featured_articles:
                if a.findChildren('a')[0]['href'] not in articles:
                    self.get_article_info(a.findChildren('a')[0]['href'])
                    articles.add(a.findChildren('a')[0]['href'])
            latest_articles = soup.find_all(href=True, class_="post-block__title__link")
            # # get all from latest articles
            for a in latest_articles:
                if a['href'] not in articles:
                    self.get_article_info(a['href'])
                    articles.add(a['href'])
            LOAD_MORE_BUTTON_XPATH = '//*[@id="tc-main-content"]/div[2]/div/div/button/span'
            try:
                loadMoreButton = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
                action = ActionChains(driver)
                action.move_to_element(loadMoreButton).click().perform()
                time.sleep(3)
            except:
                print("All articles loaded")
                load_button = False


    def get_article_info(self, article):
        #driver = webdriver.Chrome('./chromedriver')
        #driver.get(article)
        #article.click()
        #soup = BeautifulSoup(driver.page_source, 'html.parser')
        #menu_items = soup.find_all(class_='menu article__tags__menu')
        #for item in list(menu_items.children):
            #print(item.children[0].get_text())



if __name__ == '__main__':
    tcScraper = Scraper(URL)
    tcScraper.scrape()
