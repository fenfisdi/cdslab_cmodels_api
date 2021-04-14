from typing import Generator, Tuple
from pymongo import MongoClient
from pymongo.database import Database

from src.config import db_config


def api_get_db_connection(
    db_uri: str = db_config['MONGO_URI'],
) -> Generator[MongoClient, None, None]:
    """Creates connection to Mongodb server.

    Yields
    ------
    db_connection: MongoClient
        Object containing the db connection.
    """
    db_connection = MongoClient(db_uri)

    try:
        yield db_connection
    finally:
        db_connection.close()


def get_db(
    db_uri: str = db_config['MONGO_URI'],
    db_name: str = db_config['MONGO_DB']
) -> Tuple[MongoClient, Database]:
    """Gets Mongodb connection and database.

    Parameters
    ----------
    db_uri: str
        Mongo server URI.
    db_name: str
        Mongo database name.

    Returns
    -------
    db_connection : MongoClient
    db : pymongo.database.Database
    """
    db_connection = MongoClient(db_uri)
    db: Database = db_connection[db_name]

    return db_connection, db
