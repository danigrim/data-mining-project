"""
File for database utilities
Authors: Edward Mattout & Daniella Grimberg
"""

import logging
import sys

import mysql.connector
from config import HOST, DATABASE, USER, PASSWORD, LOG_FILE_FORMAT, LOG_FILE_NAME

formatter = logging.Formatter(LOG_FILE_FORMAT)

logger = logging.getLogger('database')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE_NAME)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def connect_to_database():
    """
    Function creates connection to database
    :return: cursor
    """
    try:
        connection = mysql.connector.connect(host=HOST,
                                             database=DATABASE,
                                             user=USER,
                                             password=PASSWORD)
    except mysql.connector.Error as error:
        logger.error("Error: Failed to connect to database. Exiting Program", error)
        sys.exit(1)
    logger.info("Successfully connected to database")
    return connection, connection.cursor()


def close_database_connection(connection, cursor):
    """
    Function closes connection to database
    :return: None
    """
    if connection.is_connected():
        cursor.close()
        connection.close()
        logger.info("Successfully closed database connection")


def insert_author(connection, cursor, author_name, twitter_handle):
    """
    Function inserts data into authors table
    :param connection: connection to database
    :param cursor: cursor
    :param author_name: full name of authors
    :param twitter_handle: twitter handle of author
    :return: author_id
    """
    try:
        cursor.execute("""INSERT IGNORE INTO authors (full_name, twitter_handle)
                        VALUES (%s, %s) """, (author_name, twitter_handle))
        connection.commit()
    except mysql.connector.Error as error:
        logger.error("Failed to insert into table AUTHORS {}".format(error))
    finally:
        cursor.execute("""SELECT author_id FROM authors WHERE full_name = (%s)""", (author_name,))
        res = cursor.fetchall()
        author_id = res[0][0] if res else None
        return author_id


def insert_article(connection, cursor, link, title, date):
    """
    Function inserts article to articles table
    :param connection: connection to database
    :param cursor: cursor to execute sql queries
    :param link: link of article
    :param title: title of article
    :param date: publish data of article
    :return: article_id
    """
    try:
        cursor.execute("""INSERT IGNORE INTO articles (link, title, date) 
                            VALUES (%s, %s, %s)""", (link, title, date))
        connection.commit()
    except mysql.connector.Error as error:
        logger.error("Failed to insert into table ARTICLES {}".format(error))
    finally:
        cursor.execute("""SELECT article_id FROM articles WHERE title = (%s)""", (title,))
        res = cursor.fetchall()
        article_id = res[0][0] if res else None
        return article_id


def insert_tag(connection, cursor, tag, article_id):
    """
    Function inserts tags of article to tags table
    :param connection: connection to database
    :param cursor: cursor to execute sql queries
    :param tag: tag of article
    :param article_id: article_id
    :return: None
    """
    try:
        cursor.execute("""INSERT IGNORE INTO tags (tag_text) VALUES (%s)""", (tag,))
        connection.commit()
    except mysql.connector.Error as error:
        logger.error("Failed to insert into table TAGS {}".format(error))
    finally:
        cursor.execute("""SELECT tag_id FROM tags WHERE tag_text = (%s)""", (tag,))
        res = cursor.fetchall()
        tag_id = res[0][0] if res else None
        if tag_id and article_id:
            try:
                cursor.execute("""INSERT INTO article_to_tags (article_id, tag_id) VALUES (%s, %s)""",
                               (article_id, tag_id))
                connection.commit()
            except mysql.connector.Error as error:
                logger.error("Failed to insert into table ARTICLE_TO_TAGS {}".format(error))


def insert_article_author_relation(connection, cursor, article_id, author_id):
    """
    Inserts article author relationship in database
    :param connection:
    :param cursor:
    :param article_id:
    :param author_id:
    :return: None
    """
    try:
        cursor.execute("""INSERT IGNORE INTO article_to_authors (article_id, author_id) VALUES (%s, %s)""",
                       (article_id, author_id))
        connection.commit()
    except mysql.connector.Error as error:
        logger.error("Failed to insert into table ARTICLE_TO_AUTHORS {}".format(error))


def article_in_database(cursor, title):
    """
    Function checks if article already exists in database to avoid need to search
    :param cursor:
    :param title:
    :return:
    """
    cursor.execute("""SELECT article_id FROM articles WHERE title = (%s)""", (title,))
    if cursor.fetchall():
        logger.info(f"Article with title {title} already in database!")
        return True
    return False


def insert_article_entry(author_name, twitter_handle, tag_list, title, date, link):
    """
    Function inserts article information into database
    :param author_name: name of author
    :param date: article date
    :param link article link
    :param twitter_handle: authors' twitter handle
    :param tag_list: list of tags associated to article
    :param title: title of article
    :return: None
    """
    connection, cursor = connect_to_database()
    if not article_in_database(cursor, title):
        author_id = insert_author(connection, cursor, author_name, twitter_handle)
        article_id = insert_article(connection, cursor, link, title, date)
        for tag in set(tag_list):
            insert_tag(connection, cursor, tag, article_id)
        if article_id and author_id:
            insert_article_author_relation(connection, cursor, article_id, author_id)
        else:
            logger.error(f"Error inserting author article relation for article title {title} and author {author_name}")
    close_database_connection(connection, cursor)
