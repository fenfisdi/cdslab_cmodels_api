from pymongo import MongoClient

from src.config import db_config


def api_get_db_connection():
    """Creates connection to mongodb engine

    Yields
    ------
    db_connection: MongoClient
        Object containing the db connection
    """
    db_connection = MongoClient(db_config['MONGO_URI'])

    try:
        yield db_connection
    finally:
        db_connection.close()
