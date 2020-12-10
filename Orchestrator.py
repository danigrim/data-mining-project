from Scraper import Scraper
from database import make_tables
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException
from utils import get_url
from Article import Article
from database_utils import insert_article_entry
import sys
from NewsApi import NewsApi
from datetime import datetime


class Orchestrator:
    """
    Orchestrator class used to manage tc scraper, database utilities and NewsApi
    """
    def __init__(self, tags, authors, months, display, today, limit, make_db):
        """
        Orchestrator initializer
        """
        self.tags = tags
        self.authors = authors
        self.months = months
        self.today = today
        self.display = display
        self.limit = limit
        self.articles_scraped = 0
        self.tc_scraper = initialize_scraper()
        if make_db:
            make_tables()

    def run(self):
        """
        Runs main program flow
        :return:
        """
        while self.tc_scraper.can_load_more:
            accumulated_tags = set()
            try:
                new_articles = self.tc_scraper.get_new_articles()
                for article in new_articles:
                    date, title, twitter_handle, author_name, tag_list, month = self.init_article(article)
                    satisfies_reqs = self.article_satisfies_options(date, month, author_name, tag_list)
                    if satisfies_reqs:
                        self.handle_article(author_name, twitter_handle, tag_list, title, date, article)
                        accumulated_tags.update(tag_list)
            except NoSuchWindowException as e:
                print("Error: Window not found. Make sure scraping browser was not closed", e)
            finally:
                self.get_news_api_articles(accumulated_tags)

    def init_article(self, article):
        article_entity = Article(self.tc_scraper.url, article)
        return article_entity.scrape(self.tc_scraper.driver)

    def handle_article(self, author_name, twitter_handle, tag_list, title, date, article):
        insert_article_entry(author_name, twitter_handle, tag_list, title, date, (self.tc_scraper.url + article))
        self.print_article_info(title, date, tag_list, author_name, twitter_handle)
        self.articles_scraped += 1
        self.check_exceeded_limit()

    def print_article_info(self, title, date, tags_list, author, twitter):
        """
        Prints article information according to display preferences
        :param title:
        :param date:
        :param tags_list:
        :param author:
        :param twitter:
        :return:
        """
        if self.display == "all":
            print("Title:", title, "Date:", date, "Tag_list:", tags_list, "Author Name:", author, "Twitter Handle:",
                  twitter, "\n")
        else:
            article_info = {"title": title, "date": date, "tags": tags_list, "author": author, "twitter": twitter,
                            "count": self.articles_scraped}
            print(" ".join(
                str(choice + ": " + str(article_info[choice])) for choice in self.display if choice in article_info))

    def check_exceeded_limit(self):
        """
        Function checks if article limit has exceeded based on setting
        :return: True if limited exceeded, False otherwise
        """
        if self.limit and self.articles_scraped >= self.limit:
            print("All done... ", self.tc_scraper.limit, " articles scraped")
            sys.exit(0)

    def article_satisfies_options(self, date, month, author_name, tag_list):
        """
        Function checks if article satisfies user inputted options
        :param date: article date
        :param author_name: article author
        :param tag_list: article tag list
        :return:
        """
        if self.authors != "all":
            if author_name.lower() not in self.authors:
                return False
        if self.today:
            if datetime.today().strftime("%Y/%m/%d") != date:
                return False
        if self.months != "all":
            if month not in list(map(lambda m: str(m).strip("0"), self.months)):
                return False
        if self.tags != "all":
            if not set(tag_list) & set(self.tags):
                return False
        return True

    def get_news_api_articles(self, accumulated_tags):
        n_api = NewsApi([tag for tag in accumulated_tags])
        api_article_list = n_api.get_article_list()
        for a in api_article_list:
            if n_api.article_unseen(a):
                date, month, title, author_name, tag_list, source = n_api.get_article_info(api_article_list)
                satisfies_reqs = self.article_satisfies_options(date, month, author_name, tag_list)
                if satisfies_reqs:
                    self.handle_article(author_name, "No Twitter Account", tag_list, title, date, source)


def initialize_scraper():
    tc_scraper = Scraper()
    get_url(tc_scraper.url, tc_scraper.driver)
    return tc_scraper

