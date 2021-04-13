from unittest import TestCase
from unittest.mock import patch, Mock

from mongomock import patch as db_patch
from pymongo.database import Database
from pymongo import MongoClient

from src.db.mongo import api_get_db_connection, get_db


def solve_path(path: str):
    source = 'src.config'
    return ".".join([source, path])


class MongoTestCase(TestCase):
    server = "mongodb://mongodb0.example.com:27017"

    @db_patch(servers=(('mongodb://mongodb.example.com', 27017),))
    @patch(solve_path('db_config'))
    def test_get_db_connection(self, mock_config: Mock):
        mock_config.get.side_effect = [MongoTestCase.server, "test_db"]

        db_connection_generator = api_get_db_connection(MongoTestCase.server)
        db_connection = next(db_connection_generator)

        self.assertIsInstance(db_connection, MongoClient)

        try:
            next(db_connection_generator)
        except StopIteration:
            pass
        except Exception as e:
            raise e

    @db_patch(servers=(('mongodb://mongodb.example.com', 27017),))
    @patch(solve_path('db_config'))
    def test_get_db(self, mock_config: Mock):
        mock_config.get.side_effect = [MongoTestCase.server, "test_db"]

        db_connection, db = get_db(MongoTestCase.server, "test_db")

        self.assertIsInstance(db_connection, MongoClient)
        self.assertIsInstance(db, Database)
