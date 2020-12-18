"""
File for Article class and associated functions
Authors: Edward Mattout & Daniella Grimberg
"""


from bs4 import BeautifulSoup
from config import TAGS_CLASS, ARTICLE_TAG, PARSER, LINK_TAG, LIST_ITEM, TWITTER_HANDLE_CLASS, AUTHOR_TAG
from utils import get_url


def get_twitter_handle(soup):
    """
    Function gets twitter handle from beautiful soup object
    :param soup:
    :return:
    """
    twitter = soup.find(class_=TWITTER_HANDLE_CLASS)
    twitter_handle = twitter.findChildren(ARTICLE_TAG)[0][LINK_TAG] if twitter and twitter.findChildren(ARTICLE_TAG) \
        else "No Twitter account"
    return twitter_handle


def get_author_name(soup):
    """
    Function gets author name from beautiful soup object
    :param soup: beautiful soup object
    :return: Author Name if exists else "Name not found"
    """
    author = soup.find(class_=AUTHOR_TAG)
    author_name = author.findChildren(ARTICLE_TAG)[0].get_text() if author and author.findChildren(
        ARTICLE_TAG) else "Name not found"
    return author_name


def get_tag_list(soup):
    """
    Function gets tags list of article
    :param soup: soup object
    :return: list of tags if found else empty list
    """
    menu_items = soup.find(LIST_ITEM, class_=TAGS_CLASS)
    tag_list = []
    if menu_items:
        for li in list(menu_items.children):
            tag_list.append(list(li.children)[0].get_text().lower())
    return tag_list


class Article:
    """
    Class for tech-crunch article
    """

    def __init__(self, url, title):
        """
        Article initializer
        :param title, date and tag list of article
        """
        self.url = url + title
        self.title = title

    def scrape(self, driver):
        get_url(self.url, driver)
        soup = BeautifulSoup(driver.page_source, PARSER)
        date, month, title = self.get_date_title()
        twitter_handle = get_twitter_handle(soup)
        author_name = get_author_name(soup)
        tag_list = get_tag_list(soup)
        driver.back()  # Move back to main page
        return date, title, twitter_handle, author_name, tag_list, month

    def get_date_title(self):
        """
        Function gets article date and title from url title
        :param self:
        :return: date, title or empty strings if none found
        """
        date, title, month = "", "", ""
        try:
            date, title = self.title.rsplit('/', 2)[0][1:], self.title.rsplit('/', 2)[1]
            month = date.split("/")[1].strip("0")
        except IndexError as e:
            print("Error: Unrecognized format for article date and title", e)
        finally:
            return date, month, title
