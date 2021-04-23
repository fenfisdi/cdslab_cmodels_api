from unittest import TestCase
from unittest.mock import patch, Mock

import mongomock
from mongomock import patch as db_path
from pymongo.results import InsertOneResult, DeleteResult

from src.interfaces.crud import MongoCRUD
from src.models.db.cmodels import CompartmentalModelEnum


def solve_path(path: str):
    source = 'src.db.mongo'
    return ".".join([source, path])


class MongoCRUDTestCase(TestCase):
    server = "mongodb://mongodb0.example.com:27017"

    @db_path(servers=(('server.example.com', 27017),))
    def setUp(self):
        self.client = mongomock.MongoClient('server.example.com')
        self.test_mock = self.client.db
        self.test_collection = self.test_mock.collection
        self.mongo_crud = MongoCRUD(self.client, self.test_collection)
        self._id_example = CompartmentalModelEnum.sir.value.id
        self.model_example = {'_id': self._id_example}

    def tearDown(self):
        self.client.close()

    @patch(solve_path('get_db'))
    def test_insert_ok(self, mock: Mock):
        result = self.mongo_crud.insert(self.model_example)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, InsertOneResult)

    @patch(solve_path('get_db'))
    def test_insert_no_id_present_in_document(self, mock: Mock):
        try:
            self.mongo_crud.insert(
                {'no_id_present': 'not_a_valid_query'}
            )
        except ValueError:
            self.assertTrue(True)
        else:
            self.fail('_id must be present in inserted document')

    @patch(solve_path('get_db'))
    def test_insert_existent_document(self, mock: Mock):
        self.mongo_crud.insert(self.model_example)
        try:
            self.mongo_crud.insert(self.model_example)
        except ValueError:
            self.assertTrue(True)
        else:
            self.fail('_id must be present in inserted document')

    @patch(solve_path('get_db'))
    def test_read_ok(self, mock: Mock):
        self.mongo_crud.insert(self.model_example)
        read_result = self.mongo_crud.read(self._id_example)

        self.assertIsNotNone(read_result)
        self.assertIsInstance(read_result, dict)

    @patch(solve_path('get_db'))
    def test_read_not_found(self, mock: Mock):
        result = self.mongo_crud.read(self._id_example)
        self.assertIsNone(result)

    @patch(solve_path('get_db'))
    def test_update_cmodel_state_ok(self, mock: Mock):
        self.mongo_crud.insert(self.model_example)
        new_data = {'params': ['a', 'b', 'c']}

        result = self.mongo_crud.update(
            self._id_example,
            new_data
        )

        self.assertTrue(result)

    @patch(solve_path('get_db'))
    def test_update_state_fail(self, mock: Mock):
        result = self.mongo_crud.update(self._id_example, {})

        self.assertFalse(result)

    @patch(solve_path('get_db'))
    def test_update_state_no_query(self, mock: Mock):
        result = self.mongo_crud.update(None, {})
        self.assertFalse(result)

    @patch(solve_path('get_db'))
    def test_delete_state_ok(self, mock: Mock):
        self.mongo_crud.insert(self.model_example)
        result = self.mongo_crud.delete(self._id_example)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, DeleteResult)
