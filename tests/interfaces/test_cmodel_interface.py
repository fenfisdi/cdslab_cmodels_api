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
        self.mock_interface = CModelsInterface(
            self.client, self.test_collection
        )
        self.cmodel_example_document = CompartmentalModelEnum.sir.value

    def tearDown(self):
        self.client.close()

    @patch(solve_path('get_db'))
    def test_insert_one_cmodel_document_ok(self, mock: Mock):

        result = self.mock_interface.insert_one_cmodel_document(
            self.cmodel_example_document
        )

        self.assertIsNotNone(result)
        self.assertIsInstance(result, InsertOneResult)

    @patch(solve_path('get_db'))
    def test_insert_one_cmodel_document_exists(self, mock: Mock):

        self.mock_interface.insert_one_cmodel_document(
            self.cmodel_example_document
        )

        result = self.mock_interface.insert_one_cmodel_document(
            self.cmodel_example_document
        )

        pruned_example_document = CModelsInterface._prune_db_document(
            self.cmodel_example_document.dict(by_alias=True)
        )

        self.assertEqual(
            result,
            pruned_example_document
        )

    @patch(solve_path('get_db'))
    def test_insert_one_cmodel_document_update(self, mock: Mock):

        self.mock_interface.insert_one_cmodel_document(
            self.cmodel_example_document
        )

        self.cmodel_example_document.state_variables = ['S', 'I']

        result = self.mock_interface.insert_one_cmodel_document(
            self.cmodel_example_document
        )

        self.assertIsNotNone(result)
        self.assertTrue(result)

    @patch(solve_path('get_db'))
    def test_prune_db_document(self, mock: Mock):

        _id = self.cmodel_example_document.id

        self.mock_interface.insert_one_cmodel_document(
            self.cmodel_example_document
        )

        read_model = self.mock_interface.crud.read(_id)
        pruned_document = self.mock_interface._prune_db_document(read_model)

        self.assertIsNotNone(pruned_document)

        try:
            pruned_document['inserted_at']
        except KeyError:
            self.assertTrue(True)
        else:
            self.fail('inserted_at key not expected')

        try:
            pruned_document['updated_at']
        except KeyError:
            self.assertTrue(True)
        else:
            self.fail('updated_at key not expected')

    @patch(solve_path('get_db'))
    def test_insert_all_models(self, mock: Mock):

        result = self.mock_interface.insert_all_cmodel_documents()

        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], InsertOneResult)
