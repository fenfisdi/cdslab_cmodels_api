from typing import Generator, Optional, Tuple, Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import mongomock

from src.config import settings
from src.utils.patterns import Singleton


class MongoClientSingleton(metaclass=Singleton):
    db_uri: Optional[str] = settings.get('MONGO_URI'),

    def __init__(
        self,
        db_connection: MongoClient = MongoClient(db_uri),
        db: Union[str, Database] = settings.get('MONGO_DB'),
        coll: Union[str, Collection] = settings.get('CMODELS_COLL')
    ) -> None:
        self.db_connection = db_connection
        self.db = db
        self.coll = coll

    def api_get_db_connection(self) -> Generator[MongoClient, None, None]:
        """Creates connection to Mongodb server.

        Yields
        ------
        db_connection: MongoClient
            Object containing the db connection.
        """
        try:
            yield self.db_connection
        finally:
            self.db_connection.close()

    def get_db(
        self,
        db: Optional[str] = None
    ) -> Tuple[MongoClient, Database]:
        """Gets Mongodb connection and database.

        Returns
        -------
        db_connection : MongoClient
        db : pymongo.database.Database
        """
        if db and isinstance(db, str):
            self.db = db
        return self.db_connection, self.db

    def get_collection(
        self,
        coll: Optional[str] = None
    ) -> Tuple[MongoClient, Collection]:
        """
        Returns
        -------
        db_connection: pymongo.MongoClient
        coll: pymongo.collection.Collection
        """
        if coll and isinstance(coll, str):
            self.coll = coll
        return self.db_connection, self.coll

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):                                                 # noqa
        if isinstance(value, str):
            self._db = self.db_connection[value]
        elif isinstance(value, Database) or isinstance(value, mongomock.Database):
            self._db = value

    @property
    def coll(self):
        return self._coll

    @coll.setter
    def coll(self, value):                                               # noqa
        if isinstance(value, str):
            self._coll = self.db[value]
        elif isinstance(value, Collection) or isinstance(value, mongomock.Collection):
            self._coll = value
