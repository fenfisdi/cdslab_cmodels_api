from unittest import TestCase
from unittest.mock import patch, Mock

import mongomock
from mongomock import patch as db_path
from pymongo.results import InsertOneResult

from src.interfaces.crud import MongoCRUD


def solve_path(path: str):
    source = 'src.db.mongo'
    return ".".join([source, path])


class CmodelInterfaceTestCase(TestCase):
    server = "mongodb://mongodb0.example.com:27017"

    @db_path(servers=(('server.example.com', 27017),))
    def setUp(self):
        self.client = mongomock.MongoClient('server.example.com')
        self.test_mock = self.client.db
        self.test_collection = self.test_mock.collection
        self.mongo_crud = MongoCRUD(self.client, self.test_collection)

    def tearDown(self):
        self.client.close()

    @patch(solve_path('get_db'))
    def test_insert_cmodel_ok(self, mock: Mock):
        model = {"_id": "example"}

        result = self.mongo_crud.insert_cmodel(model)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, InsertOneResult)

    @patch(solve_path('get_db'))
    def test_read_cmodel_ok(self, mock: Mock):
        model = {"_id": "example"}

        self.mongo_crud.insert_cmodel(model)
        read_result = self.mongo_crud.read_model(model)

        self.assertIsNotNone(read_result)
        self.assertIsInstance(read_result, dict)

    @patch(solve_path('get_db'))
    def test_read_cmodel_not_found(self, mock: Mock):
        model = {"_id": "example"}
        result = self.mongo_crud.read_model(model)
        self.assertIsNone(result)

    @patch(solve_path('get_db'))
    def test_update_cmodel_state_ok(self, mock: Mock):
        model = {"_id": "example"}

        self.mongo_crud.insert_cmodel(model)
        new_data = {'params': ['a', 'b', 'c']}

        result = self.mongo_crud.update_model(model, new_data)

        self.assertTrue(result)

    @patch(solve_path('get_db'))
    def test_update_cmodel_state_fail(self, mock: Mock):
        query = {'_id': 'test_example'}

        result = self.mongo_crud.update_model(query, {})

        self.assertFalse(result)
