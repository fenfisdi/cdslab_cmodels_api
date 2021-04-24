
from src.db.mongo import MongoClientSingleton
from unittest import TestCase
from unittest.mock import patch, Mock

import mongomock
from mongomock import patch as db_path

from src.use_cases.cmodels import CmodelUseCases
from src.interfaces.crud import MongoCRUD
from src.models.db.cmodels import CompartmentalModelEnum


class CmodelUseCasesTestCase(TestCase):

    @db_path(servers=(('server.example.com', 27017),))
    def setUp(self):
        self.connection_mock = mongomock.MongoClient('server.example.com')
        self.db_mock = self.connection_mock.db
        self.collection_mock = self.db_mock.collection
        self.mongo_singleton_mock = MongoClientSingleton(
            db_connection=self.connection_mock,
            db=self.db_mock,
            coll=self.collection_mock
        )
        self.mongo_crud_mock = MongoCRUD(
            *self.mongo_singleton_mock.get_collection()
        )
        self.cmodel_use_cases = CmodelUseCases(self.mongo_singleton_mock)

    def tearDown(self):
        self.connection_mock.close()

    @patch('src.config.db_config')
    def test_cmodels_in_ok(self, mock: Mock):
        self.cmodel_use_cases.update_cmodels_collection()
        for model in CompartmentalModelEnum.values():
            result = self.mongo_crud_mock.read(model.id)
            self.assertIsNotNone(result)
