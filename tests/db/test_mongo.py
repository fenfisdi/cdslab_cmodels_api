from unittest import TestCase
from unittest.mock import patch, Mock

import mongomock
from mongomock import patch as db_path
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from src.db.mongo import MongoClientSingleton


def solve_path(path: str):
    source = 'src.config'
    return ".".join([source, path])


class MongoTestCase(TestCase):

    @db_path(servers=(('server.example.com', 27017),))
    def setUp(self):
        self.connection_mock = mongomock.MongoClient('server.example.com')
        self.db_mock = self.connection_mock.db
        self.collection_mock = self.db_mock.collection
        self.mongo_singleton_mock = MongoClientSingleton(
            self.connection_mock, self.db_mock, self.collection_mock
        )

    def tearDown(self):
        self.connection_mock.close()

    @patch(solve_path('db_config'))
    def test_get_db_connection(self, mock: Mock):
        db_connection_gen = self.mongo_singleton_mock.api_get_db_connection()
        db_connection = next(db_connection_gen)

        self.assertIsInstance(db_connection, MongoClient)

        with self.assertRaises(StopIteration):
            next(db_connection_gen)

    @patch(solve_path('db_config'))
    def test_get_db(self, mock_config: Mock):
        db_connection, db = self.mongo_singleton_mock.get_db(
            "test_db"
        )

        self.assertIsInstance(db_connection, MongoClient)
        self.assertIsInstance(db, Database)

    @patch(solve_path('db_config'))
    def test_get_collection(self, mock_config: Mock):

        db_connection, coll = self.mongo_singleton_mock.get_collection()

        self.assertIsInstance(db_connection, MongoClient)
        self.assertIsInstance(coll, Collection)
