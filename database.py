"""
File initializes database tables given configuration parameters
Authors: Edward Mattout & Daniella Grimberg
"""

import mysql.connector
from database_utils import connect_to_database, close_database_connection, LOG_FILE_FORMAT, LOG_FILE_NAME
import sys
import logging

formatter = logging.Formatter(LOG_FILE_FORMAT)

logger = logging.getLogger('database_init')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE_NAME)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def make_tables():
    """
    Function creates database tables
    :return:
    """
    try:
        connection, cursor = connect_to_database()
        if not connection and cursor:
            raise mysql.connector.Error("No connection")
        cursor.execute( """CREATE TABLE authors (
                author_id INT NOT NULL AUTO_INCREMENT,
                full_name VARCHAR(45) UNIQUE,
                twitter_handle VARCHAR(45),
                PRIMARY KEY (author_id))""");
        cursor.execute( """CREATE TABLE articles (
                article_id INT NOT NULL AUTO_INCREMENT,
                link VARCHAR(250) UNIQUE,
                title VARCHAR(250) UNIQUE,
                date DATETIME,
                PRIMARY KEY (article_id))""");
        cursor.execute("""CREATE TABLE tags (
                    tag_id INT NOT NULL AUTO_INCREMENT,
                    tag_text VARCHAR(45) UNIQUE,
                    PRIMARY KEY (tag_id))
                    """);
        cursor.execute("""CREATE TABLE article_to_tags (
                    id INT NOT NULL AUTO_INCREMENT,
                    article_id INT,
                    tag_id INT, 
                    CONSTRAINT article_id_tag FOREIGN KEY (article_id)
                    REFERENCES articles(article_id) ON DELETE CASCADE,
                    CONSTRAINT tag_id_article FOREIGN KEY (tag_id)
                    REFERENCES tags(tag_id) ON DELETE CASCADE,
                    PRIMARY KEY (id)
                    )""");
        cursor.execute("""CREATE TABLE article_to_authors (
                    id INT NOT NULL AUTO_INCREMENT,
                    article_id INT,
                    author_id INT,
                    FOREIGN KEY (article_id) REFERENCES articles(article_id),
                    FOREIGN KEY (author_id) REFERENCES authors(author_id),
                    PRIMARY KEY (id)
                    )""");
        logger.info("Succesfully created tables in database")
    except mysql.connector.Error as error:
        logger.error("Failed to create table in MySQL: {}".format(error))
    finally:
        close_database_connection(connection, cursor)


if __name__ == '__main__':
    make_tables()

