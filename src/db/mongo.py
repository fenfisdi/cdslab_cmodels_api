from pymongo import MongoClient
from pymongo.database import Database

from src.config import db_config


def get_db_connection() -> Database:
    """Creates database connection to mongo engine

    Yields
    ------
    db_connection: MongoClient
        Object containing the db connection
    """
    db_connection = MongoClient(
        db_config['MONGO_HOST'],
        db_config['MONGO_PORT']
    )

    try:
        yield db_connection
    finally:
        db_connection.close()
