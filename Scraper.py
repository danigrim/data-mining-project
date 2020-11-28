from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from config import URL, CLASS_FEATURED_ARTICLES, TAG_FEATURED_ARTICLES, CLASS_LATEST_ARTICLES, LOAD_MORE_BUTTON_XPATH, \
    TAGS_CLASS, ARTICLE_TAG, LINK_TAG, PARSER, LIST_ITEM


class Scraper:
    """
    Scraper class used to scrape techcrunch
    """

    def __init__(self, url):
        """
        Scraper initializer
        :param url: url to website
        """
        self.url = url

    def scrape(self):
        """
        Function uses a selenium chrome driver in order to scrape main page of techcrunch.
        While there are more articles to load, navigates to each article, scraping  for tags, date, and title
        Presses load more button
        """
        driver = webdriver.Chrome('./chromedriver')
        driver.get(self.url)

        articles = set()
        load_button = True
        while load_button:
            soup = BeautifulSoup(driver.page_source, PARSER)  # re initialize beautiful soup after load more pressed
            # finds articles in featured category
            all_articles = [a.findChildren(ARTICLE_TAG)[0] for a in soup.find_all(TAG_FEATURED_ARTICLES,
                                                                                  class_=CLASS_FEATURED_ARTICLES)]
            # finds articles in 'latest' category
            all_articles.extend(soup.find_all(href=True, class_=CLASS_LATEST_ARTICLES))
            for a in all_articles:
                if a[LINK_TAG] not in articles:
                    self.get_article_info(a[LINK_TAG], driver)
                    articles.add(a[LINK_TAG])
            load_button = self.load_more_posts(driver)

    def load_more_posts(self, driver):
        """
        Function loads more posts as long as there is still a load more button.
        :param driver: Chrome driver
        :return: True if load more button found, False otherwise
        """
        try:
            load_more_button = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
        except NoSuchElementException as e:
            print(e)
            return False
        action = ActionChains(driver)
        action.move_to_element(load_more_button).click().perform()
        print("Loading more posts...")
        time.sleep(3)
        return True

    def get_article_info(self, article, driver):
        """
        Function prints the relevant info about each article.
        :param: article : url to relevant article, driver: chrome driver
        """
        driver.get(self.url + article)
        soup = BeautifulSoup(driver.page_source, PARSER)
        date, title = article.rsplit('/', 2)[0][1:], article.rsplit('/', 2)[1]  # Find date and title of article from
        # URL
        twitter = soup.find(class_="article__byline__meta")
        twitter_handle = twitter.findChildren(ARTICLE_TAG)[0][LINK_TAG] if twitter.findChildren(ARTICLE_TAG) else ""
        menu_items = soup.find(LIST_ITEM, class_=TAGS_CLASS)
        tag_list = []
        if menu_items:
            for li in list(menu_items.children):
                tag_list.append(list(li.children)[0].get_text())

        print("Title:", title, "Date:", date, "Tag_list:", tag_list, "Twitter Handle:", twitter_handle, "\n")
        driver.back()  # Move back to main page


class Article:
    """
    Class for tech-crunch article
    """

    def __init__(self, title, date, tag_list):
        """
        Article initializer
        :param title, date and tag list of article
        """
        self.title = title
        self.date = date
        self.tag_list = tag_list


if __name__ == '__main__':
    tcScraper = Scraper(URL)
    tcScraper.scrape()
