import mysql.connector
from mysql.connector import Error
from database_utils import connect_to_database, close_database_connection


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
                    FOREIGN KEY (article_id) REFERENCES articles(article_id), 
                    FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
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
    except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))

    finally:
        close_database_connection(connection, cursor)


if __name__ == '__main__':
    make_tables()

