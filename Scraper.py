from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sqlalchemy
from datetime import datetime
from utils import get_url
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException
import sys
from selenium.webdriver.common.action_chains import ActionChains
from Article import Article
from config import URL, CLASS_FEATURED_ARTICLES, TAG_FEATURED_ARTICLES, CLASS_LATEST_ARTICLES, LOAD_MORE_BUTTON_XPATH, \
    TAGS_CLASS, ARTICLE_TAG, LINK_TAG, PARSER, LIST_ITEM, TWITTER_HANDLE_CLASS, LOADING_TIME, AUTHOR_TAG


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

    def __init__(self, tags, authors, months, display, today, limit):
        """
        Scraper initializer
        """
        self.tags = tags
        self.authors = authors
        self.months = months
        self.display = display
        self.today = today
        self.limit = limit

    def scrape(self):
        """
        Function uses a selenium chrome driver in order to scrape main page of techcrunch.
        While there are more articles to load, navigates to each article, scraping  for tags, date, and title
        Presses load more button
        """
        driver = webdriver.Chrome('./chromedriver')
        get_url(self.url, driver)
        articles = set()
        load_button = True
        while load_button:
            soup = BeautifulSoup(driver.page_source, PARSER)  # re initialize beautiful soup after load more pressed
            # finds articles in featured category
            all_articles = [a.findChildren(ARTICLE_TAG)[0] for a in soup.find_all(TAG_FEATURED_ARTICLES,
                                                                                  class_=CLASS_FEATURED_ARTICLES)]
            # finds articles in 'latest' category
            all_articles.extend(soup.find_all(href=True, class_=CLASS_LATEST_ARTICLES))
            articles_scraped = 0
            for a in all_articles:
                if a[LINK_TAG] not in articles:
                    articles_scraped += self.get_article_info(a[LINK_TAG], driver)
                    if self.limit and articles_scraped >= self.limit:
                        print("All done... ", self.limit, " articles scraped")
                        sys.exit(0)
                    articles.add(a[LINK_TAG])
            load_button = load_more_posts(driver)

    def article_satisfies_options(self, date, author_name, tag_list):
        if self.authors != "all":
            if author_name.lower() not in self.authors:
                return False
        if self.today:
            if datetime.today().strftime("%Y/%m/%d") != date:
                return False
        if self.months != "all":
            if date.split("/")[1].strip("0") not in list(map(lambda m: str(m).strip("0"), self.months)):
                return False
        if self.tags != "all":
            if not set(tag_list) & set(self.tags):
                return False
        return True

    def get_article_info(self, article, driver):
        """
        Function prints the relevant info about each article.
        :param: article : url to relevant article, driver: chrome driver
        """
        article = Article(self.url, article)
        date, title, twitter_handle, author_name, tag_list = article.scrape(driver)
        if not self.article_satisfies_options(date, author_name, tag_list):
            return 0
        self.print_article_info(title, date, tag_list, author_name, twitter_handle)
        return 1

    def print_article_info(self,title, date, tags_list, author, twitter):
        """
        Function prints article information according to scraper settings of display
        :param title: article title
        :param date: article date YYYY/MM/DD
        :param tag_list: tags list of article
        :param author_name: author name
        :param twitter_handle: twitter handle link
        :return: None
        """
        if self.display == "all":
            print("Title:", title, "Date:", date, "Tag_list:", tags_list, "Author Name:", author, "Twitter Handle:",
              twitter, "\n")
        else:
            article_info = {"title": title, "date": date, "tags": tags_list, "author": author, "twitter": twitter}
            print(" ".join(str(choice + ": " + str(article_info[choice])) for choice in self.display if choice in article_info))