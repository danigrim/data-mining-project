#Tags and Classes for Scraper
CLASS_FEATURED_ARTICLES = 'mini-view__item__title'
TAG_FEATURED_ARTICLES = 'h3'
CLASS_LATEST_ARTICLES = 'post-block__title__link'
LOAD_MORE_BUTTON_XPATH = '//*[@id="tc-main-content"]/div[2]/div/div/button/span'
TAGS_CLASS = 'menu article__tags__menu'
ARTICLE_TAG = 'a'
LINK_TAG = 'href'
PARSER = 'html.parser'
LIST_ITEM = 'ul'
TWITTER_HANDLE_CLASS = "article__byline__meta"
AUTHOR_TAG = "article__byline"

#Scraper configurations
DISPLAY_OPTIONS = ["all", "tags", "title", "date", "author", "twitter", "count"]
LOADING_TIME = 5
URL = 'https://techcrunch.com/'

#Database configurations
HOST = 'localhost'
DATABASE = 'techcrunch_cp_2'
USER = 'root'
PASSWORD = 'newpass'