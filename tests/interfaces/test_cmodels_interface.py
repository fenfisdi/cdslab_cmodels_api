from unittest import TestCase
from unittest.mock import patch, Mock

import pymongo
from mongomock import patch as db_path
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
    def test_insert_cmodel_ok(self, mock_db: Mock):
        mock_db.return_value = self.client, self.test_mock

        model = {"_id": "example"}

        result = CmodelInterface.insert_cmodel(model)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, InsertOneResult)

    @patch(solve_path('get_db'))
    def test_read_cmodel_ok(self, mock_db: Mock):
        mock_db.return_value = self.client, self.test_mock
        query = {"_id": "example"}

        result = CmodelInterface.read_model(query)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    @patch(solve_path('get_db'))
    def test_read_cmodel_not_found(self, mock_db: Mock):
        mock_db.return_value = self.client, self.test_mock

        result = CmodelInterface.read_model({"_id": 'test_model_example'})

        self.assertIsNone(result)

    @patch(solve_path('get_db'))
    def test_update_cmodel_state_ok(self, mock_db: Mock):
        mock_db.return_value = self.client, self.test_mock
        query = {"_id": "example"}
        data = {'params': ['a', 'b', 'c']}

        result = CmodelInterface.update_model(query, data)

        self.assertTrue(result)

    @patch(solve_path('get_db'))
    def test_update_cmodel_state_fail(self, mock_db: Mock):
        mock_db.return_value = self.client, self.test_mock
        query = {'_id': 'test_example'}
        data = {'params': ['a', 'b', 'c']}

        result = CmodelInterface.update_model(query, data)

        self.assertFalse(result)

    @patch(solve_path('get_db'))
    def test_delete_cmodel(self, mock_db: Mock):
        mock_db.return_value = self.client, self.test_mock
        query = {"_id": "example"}

        result = CmodelInterface.delete_model(query)

        self.assertTrue(result)
