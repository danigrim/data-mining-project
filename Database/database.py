from sqlalchemy import ForeignKey, UniqueConstraint, create_engine
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


def get_engine():
    return create_engine(SQL_URL, echo=False)


def create_database():
    engine = get_engine()
    engine.execute(f"CREATE DATABASE {DB_NAME}")


def use_database():
    engine = get_engine()
    engine.execute(f"USE {DB_NAME}")


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)


def drop_tables():
    engine = create_engine(SQL_URL, echo=True)
    Base.metadata.drop_all(engine)


def sql_session():
    engine = sql_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


def sql_engine():
    engine = create_engine(SQL_URL, echo=True)
    return engine

def get_engine():
    return create_engine(SQL_URL, echo=False)


def create_database():
    engine = get_engine()
    engine.execute(f"CREATE DATABASE {DB_NAME}")


def use_database():
    engine = get_engine()
    engine.execute(f"USE {DB_NAME}")


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)


def drop_tables():
    engine = create_engine(SQL_URL, echo=True)
    Base.metadata.drop_all(engine)


def sql_session():
    engine = sql_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


def sql_engine():
    engine = create_engine(SQL_URL, echo=True)
    return engine
Base = declarative_base()