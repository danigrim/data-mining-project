from config import HOST, DATABASE, USER, PASSWORD
import mysql.connector
from mysql.connector import Error


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
        print("Error: Failed to connect to database", error)
    return connection, connection.cursor()


def close_database_connection(connection, cursor):
    """
    Function closes connection to database
    :return:
    """
    if connection.is_connected():
        cursor.close()
        connection.close()


def insert_article_entry(author_name, twitter_handle, tag_list, title, date ,link):
    """
    Function inserts article information into database
    :param author_name: name of author
    :param twitter_handle: authors' twitter handle
    :param tag_list: list of tags associated to article
    :param title: title of article
    :return: None
    """

    connection, cursor = connect_to_database()
    try:
        cursor.execute("""INSERT INTO authors (full_name, twitter_handle)
                        VALUES (%s, %s) """, (author_name, twitter_handle))
        author_id = cursor.lastrowid
        connection.commit()
    except mysql.connector.Error as error:
        cursor.execute("""SELECT author_id FROM authors WHERE full_name = (%s)""", (author_name,))
        author_id = cursor.fetchall()[0][0]
        print("Failed to insert into table AUTHORS {}".format(error))
    try:
        cursor.execute("""INSERT INTO articles (link, title, date) 
                            VALUES (%s, %s, %s)""", (link, title, date))
        article_id = cursor.lastrowid
    except mysql.connector.Error as error:
        print("Failed to insert into table ARTICLES {}".format(error))
        cursor.execute("""SELECT aricle_id FROM articles WHERE title = (%s)""", (title,))
        article_id = cursor.fetchall()[0][0]

    for tag in tag_list:
        try:
            cursor.execute("""INSERT INTO tags (tag_text)
                        VALUES (%s)""", (tag,))
            connection.commit()
            tag_id = cursor.lastrowid
        except mysql.connector.Error as error:
            print("Failed to insert into table TAGS {}".format(error))
            cursor.execute("""SELECT tag_id FROM tags WHERE tag_text = (%s)""", (tag,))
            tag_id = cursor.fetchall()[0][0]
    ##
    try:
        tags = """INSERT IGNORE INTO article_to_tags (article_id, tag_id) VALUES (%s, %s))"""
        cursor.execute(tags, (str(tag_list)[1:-1]).replace("'", ""))
        articles = """INSERT IGNORE INTO articles (title, link, date)
                 VALUES (%s, %s, %s)"""
    except mysql.connector.Error as error:
        print("Failed to insert into table TAGS {}".format(error))
    finally:
        close_database_connection(connection, cursor)