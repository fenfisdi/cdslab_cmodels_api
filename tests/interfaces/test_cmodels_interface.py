from unittest import TestCase
from unittest.mock import patch, Mock

import pymongo
from mongomock import patch as db_path, ObjectId
from pymongo.results import InsertOneResult

from src.interfaces.cmodel_interface import CmodelInterface
from src.db.mongo import api_get_db_connection, get_db


def solve_path(path: str):
    source = 'src.interfaces.cmodel_interface'
    return ".".join([source, path])


class CmodelInterfaceTestCase(TestCase):

    @db_path(servers=(('mongodb.example.com', 27017),))
    def setUp(self):
        self.client = pymongo.MongoClient('mongodb.example.com')
        self.test_mock = self.client.get_database('test')
        self.test_collection = self.test_mock.get_collection('cmodels')

    def tearDown(self):
        self.client.close()

    @patch(solve_path('get_db'))
    def test_insert_cmodel_documents_ok(self, mock_db: Mock):
        mock_db.return_value = self.client, self.test_mock

        model = [{"_id": "example"}]

        result = CmodelInterface.insert_cmodels_documents(model)

        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], InsertOneResult)
    """
    @patch(solve_path('get_db'))
    def test_insert_cmodel_documents_false(self, mock_db: Mock):
        mock_db.return_value = self.client, self.test_mock
        model = [{"_id": "example"}]
        self.test_client.insert_one(model[0])

        result = CmodelInterface.insert_cmodels_documents(model)

        self.assertFalse(result)
    """
