# Tags and Classes for Scraper
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

# Scraper configurations
DISPLAY_OPTIONS = ["all", "tags", "title", "date", "author", "twitter", "count"]
LOADING_TIME = 5
URL = 'https://techcrunch.com/'

# Database configurations
HOST = 'http://10.0.2.2/'
DATABASE = 'techcrunch_cp_2'
USER = 'root'
PASSWORD = 'newpass'
LOG_FILE_FORMAT = '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s'
LOG_FILE_NAME = "tc_db.log"

# Gnews configuration
API_KEY = '77dac3ede38db75a8712d54760dd2b42'
API_BASE_URL = 'https://gnews.io/api/v4/search?'
STATUS_OK = 'ok'
ARTICLE_PARAM = 'articles'
NUM_ARTICLES_PARAM = 'totalArticles'
AUTHOR_PARAM = 'author'
TITLE_PARAM = 'title'
DATE_PARAM = 'publishedAt'
LOG_FILE_NAME_API = 'gnews.log'
URL_PARAM = 'url'
API_ERROR_TAG = 'errors'
