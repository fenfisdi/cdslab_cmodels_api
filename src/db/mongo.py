from typing import Generator, Tuple

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from src.config import db_config
from src.utils.patterns import Singleton


class MongoConnection(metaclass=Singleton):
    db_uri = db_config.get('MONGO_URI')
    db_name = db_config.get('MONGO_DB')
    collection_name = db_config.get('CMODELS_COLL')

    def api_get_db_connection(self) -> Generator[MongoClient, None, None]:
        """Creates connection to Mongodb server.

        Yields
        ------
        db_connection: MongoClient
            Object containing the db connection.
        """
        db_connection = MongoClient(self.db_uri)

        try:
            yield db_connection
        finally:
            db_connection.close()

    def get_db(self) -> Tuple[MongoClient, Database]:
        """Gets Mongodb connection and database.

        Returns
        -------
        db_connection : MongoClient
        db : pymongo.database.Database
        """
        db_connection = MongoClient(self.db_uri)
        db: Database = db_connection[self.db_name]

        return db_connection, db

    def get_collection(
            self,
            collection_name: str = None
    ) -> Tuple[MongoClient, Collection]:
        """
        Returns
        -------
        db_connection: pymongo.MongoClient
        coll: pymongo.collection.Collection
        """
        if not collection_name:
            collection_name = self.collection_name
            pass
        db_connection, db = self.get_db()
        coll: Collection = db[collection_name]
        return db_connection, coll
