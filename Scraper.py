"""
File for Scraper class and its functions
Authors: Edward Mattout & Daniella Grimberg
"""

import time

from bs4 import BeautifulSoup
from config import URL, ARTICLE_TAG, LINK_TAG, CLASS_FEATURED_ARTICLES, TAG_FEATURED_ARTICLES, CLASS_LATEST_ARTICLES, \
    LOAD_MORE_BUTTON_XPATH, PARSER, LOADING_TIME
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


def load_more_posts(driver):
    """
    Function loads more posts as long as there is still a load more button.
    :param driver: Chrome driver
    :return: True if load more button found, False otherwise
    """
    try:
        load_more_button = driver.find_element_by_xpath(LOAD_MORE_BUTTON_XPATH)
    except NoSuchElementException as e:
        print("Error: Load more button not found", e)
        return False
    action = ActionChains(driver)
    action.move_to_element(load_more_button).click().perform()
    print("Loading more posts...")
    time.sleep(LOADING_TIME)
    return True


class Scraper:
    """
    Scraper class used to scrape techcrunch
    """
    url = URL

    def __init__(self):
        """
        Scraper initializer
        """
        self.can_load_more = True
        self.articles = set()
        self.driver = webdriver.Chrome('./chromedriver')

    def get_new_articles(self):
        """
        Function fetches all new links in the current driver page and returns a set with links
        :returns: set of new article links
        """
        soup = BeautifulSoup(self.driver.page_source, PARSER)  # re initialize beautiful soup after load more pressed
        # finds articles in featured category
        all_articles = [a.findChildren(ARTICLE_TAG)[0] for a in soup.find_all(TAG_FEATURED_ARTICLES,
                                                                              class_=CLASS_FEATURED_ARTICLES)]
        # finds articles in 'latest' category
        all_articles.extend(soup.find_all(href=True, class_=CLASS_LATEST_ARTICLES))
        new_articles = set()
        for a in all_articles:
            if a[LINK_TAG] not in self.articles:
                new_articles.add(a[LINK_TAG])
                self.articles.add(a[LINK_TAG])
        self.can_load_more = load_more_posts(self.driver)
        return new_articles
