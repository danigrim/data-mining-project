from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains

URL = 'https://techcrunch.com/'
CLASS_FEATURED_ARTICLES ='mini-view__item__title'
TAG_FEATURED_ARTICLES = 'h3'
CLASS_LATEST_ARTICLES = 'post-block__title__link'
LOAD_MORE_BUTTON_XPATH = '//*[@id="tc-main-content"]/div[2]/div/div/button/span'

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
            all_articles  = [a.findChildren('a')[0] for a in soup.find_all(TAG_FEATURED_ARTICLES, class_=CLASS_FEATURED_ARTICLES)]
            all_articles.extend(soup.find_all(href=True, class_=CLASS_LATEST_ARTICLES))
            for a in all_articles:
                if a['href'] not in articles:
                    self.get_article_info(a['href'], driver)
                    articles.add(a['href'])
            self.load_more_posts(driver)


    def load_more_posts(self, driver):
            loadMoreButton = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
            action = ActionChains(driver)
            action.move_to_element(loadMoreButton).click().perform()
            print("Loading more posts...")
            time.sleep(3)


    def get_article_info(self, article, driver):
        driver.get(self.url + article)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        date, title = article.rsplit('/', 2)[0][1:], article.rsplit('/', 2)[1]

        menu_items = soup.find('ul', class_='menu article__tags__menu')
        tag_list = []
        if menu_items:
            for li in list(menu_items.children):
                tag_list.append(list(li.children)[0].get_text())
        print("Title:", title, "Date:", date, "Tag_list:", tag_list)
        driver.back()


if __name__ == '__main__':
    tcScraper = Scraper(URL)
    tcScraper.scrape()
