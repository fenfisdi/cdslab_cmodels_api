
from unittest import TestCase
from unittest.mock import patch, Mock

import mongomock
from mongomock import patch as db_path

from src.use_cases.cmodels import CmodelUseCases
from src.interfaces.crud import MongoCRUD
from src.interfaces.cmodels import CModelsInterface
from src.models.db.cmodels import CompartmentalModelEnum


class CmodelUseCasesTestCase(TestCase):
    server = "mongodb://mongodb0.example.com:27017"

    @db_path(servers=(('server.example.com', 27017),))
    def setUp(self):
        self.connection_mock = mongomock.MongoClient('server.example.com')
        self.db_mock = self.connection_mock.db
        self.collection_mock = self.db_mock.collection
        self.mongo_crud_mock = MongoCRUD(
            self.connection_mock, self.collection_mock
        )
        self.cmodels_interface_mock = CModelsInterface(
            self.connection_mock, self.collection_mock
        )
        CmodelUseCases.update_cmodels_collection(
            self.cmodels_interface_mock
        )

    def tearDown(self):
        self.connection_mock.close()

    @patch('src.db.mongo.get_db')
    def test_cmodels_in_ok(self, mock: Mock):
        for model in CompartmentalModelEnum.values():
            result = self.mongo_crud_mock.read(model.id)
            self.assertIsNotNone(result)
