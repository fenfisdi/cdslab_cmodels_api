from unittest import TestCase
from unittest.mock import patch, Mock

import mongomock
from mongomock import patch as db_path
from pymongo.results import InsertOneResult

from src.interfaces.crud import MongoCRUD
from src.interfaces.cmodels import CModelsInterface
from src.models.db.cmodels import (
    CompartmentalModelEnum
)


def solve_path(path: str):
    source = 'src.db.mongo'
    return ".".join([source, path])


class CModelsInterfaceTestCase(TestCase):
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
    def test_insert_one_cmodel_document(self, mock: Mock):

        result = CModelsInterface(self.client, self.test_collection).insert_one_cmodel_document(
            CompartmentalModelEnum.values()[1])

        self.assertIsInstance(result, InsertOneResult)
