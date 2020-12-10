"""
File for News Api class, makes get requests to GNewsApi to get articles
Authors: Daniella Grimberg & Edward Mattout
"""

from config import API_KEY, API_BASE_URL, LOG_FILE_FORMAT,LOG_FILE_NAME_API, STATUS_OK, \
    ARTICLE_PARAM, AUTHOR_PARAM, TITLE_PARAM, DATE_PARAM, URL_PARAM, NUM_ARTICLES_PARAM, API_ERROR_TAG
import sys
import requests
import json
import logging

formatter = logging.Formatter(LOG_FILE_FORMAT)

logger = logging.getLogger('newsapi')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE_NAME_API)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class NewsApi:
    """
    Class used to make get requests to GNewsAPi
    """
    base_url = API_BASE_URL

    def __init__(self, tags=[]):
        """
        Api Interaction initialzier
        :params: tags list to search for
        """
        self.tags = list(tags)
        self.articles = set()

    def get_article_list(self):
        """
        Make get request to api fetch list of articles
        :return: list with article entry information
        """
        article_list = []
        for tag in self.tags:
            if len(tag) > 4 and not tag.count(" "):
                url = self.base_url + f"q=\"{tag}\"" + f"&token={API_KEY}"
                resp = json.loads(requests.get(url).content)
                if API_ERROR_TAG in resp:
                    error = resp[API_ERROR_TAG]
                    logger.info(f'Unable to make get request to Gnews, response: {error}')
                elif resp[NUM_ARTICLES_PARAM] > 0:
                    articles = resp[ARTICLE_PARAM]
                    for item in articles:
                        item.update({"tag": tag})
                    article_list.extend(articles)
        return article_list if article_list else []

    def get_article_info(self, article):
        """
        Function gets information of article entry
        :param article: dictionary of article
        :return: date, month, title, author, tags_list, url
        """
        title = article[TITLE_PARAM]
        url = article[URL_PARAM]
        author = article['source']['name']
        tags_list = article['tag']
        date = article[DATE_PARAM]
        month = date.split("-")[1]
        self.articles.add(title)
        return date, month, title, author, tags_list, url

    def article_unseen(self, article):
        """
        Function checks if article has been printed and added yet
        :param article:
        :return:
        """
        return article[TITLE_PARAM] not in self.articles