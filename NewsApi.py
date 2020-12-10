"""
File for News Api class, makes get requests to NewsApi to get articles
Authors: Daniella Grimberg & Edward Mattout
"""

from config import API_KEY, API_BASE_URL, LOG_FILE_FORMAT,LOG_FILE_NAME_API, STATUS_OK, \
    ARTICLE_PARAM, AUTHOR_PARAM, TITLE_PARAM, DATE_PARAM
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
    Class used to make get requests to NewsApi
    """
    base_url = API_BASE_URL

    def __init__(self, tags=[]):
        """
        Api Interaction initialzier
        """
        self.tags = list(tags)
        self.articles = set()


    def get_article_list(self):
        """
        Make get request to api fetch list of articles
        :return:
        """
        article_list = []
        for tag in self.tags:
            url = self.base_url + f"&q={tag}" + f"&apikey={API_KEY}"
            resp = json.loads(requests.get(url).content)
            if resp['status'] != STATUS_OK:
                r_s = resp['status']
                logger.info(f'Unable to make get request to NewsAPI status code: {r_s}, url attempted: {url}')
                return []
            article_list.append(resp[ARTICLE_PARAM])
        return article_list[0] if article_list else []


    def get_article_info(self, article):
        title = article[TITLE_PARAM]
        source = article['source']['name']
        author = article[AUTHOR_PARAM]
        tags_list = self.tags
        date = article[DATE_PARAM]
        month = date.split("-")[1]
        self.articles.add(title)
        return date, month, title, author, tags_list, source

    def article_unseen(self, article):
        """
        :param article:
        :return:
        """
        return article[TITLE_PARAM] not in self.articles