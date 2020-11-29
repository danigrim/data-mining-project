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


def insert_author(connection, cursor, author_name, twitter_handle):
    try:
        cursor.execute("""INSERT IGNORE INTO authors (full_name, twitter_handle)
                        VALUES (%s, %s) """, (author_name, twitter_handle))
        connection.commit()
    except mysql.connector.Error as error:
        print("Failed to insert into table AUTHORS {}".format(error))
    finally:
        cursor.execute("""SELECT author_id FROM authors WHERE full_name = (%s)""", (author_name,))
        res = cursor.fetchall()
        author_id = res[0][0] if res else None
        return author_id


def insert_article(connection, cursor, link, title, date):
    try:
        cursor.execute("""INSERT IGNORE INTO articles (link, title, date) 
                            VALUES (%s, %s, %s)""", (link, title, date))
        connection.commit()
    except mysql.connector.Error as error:
        print("Failed to insert into table ARTICLES {}".format(error))
    finally:
        cursor.execute("""SELECT article_id FROM articles WHERE title = (%s)""", (title,))
        res = cursor.fetchall()
        article_id = res[0][0] if res else None
        return article_id


def insert_tag(connection, cursor, tag, article_id):
    try:
        cursor.execute("""INSERT IGNORE INTO tags (tag_text) VALUES (%s)""", (tag,))
        connection.commit()
    except mysql.connector.Error as error:
        print("Failed to insert into table TAGS {}".format(error))
    finally:
        cursor.execute("""SELECT tag_id FROM tags WHERE tag_text = (%s)""", (tag,))
        res = cursor.fetchall()
        tag_id = int(res[0][0]) if res else None
        if tag_id and article_id:
            try:
                cursor.execute("INSERT INTO article_to_tags (article_id, tag_id) VALUES (5, 1))")
                connection.commit()
            except mysql.connector.Error as error:
                print("Failed to insert into table ARTICLE_TO_TAGS {}".format(error))


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
    author_id = insert_author(connection, cursor, author_name, twitter_handle)
    article_id = insert_article(connection, cursor, link, title, date)
    for tag in tag_list:
        insert_tag(connection, cursor, tag, article_id)
    # try:
    #     cursor.execute("""INSERT IGNORE INTO article_to_authors (article_id, author_id) VALUES (?, ?))""", (article_id, author_id))
    #     connection.commit()
    # except mysql.connector.Error as error:
    #     print("Failed to insert into table ARTICLE_TO_AUTHORS {}".format(error))
   # finally:
    close_database_connection(connection, cursor)