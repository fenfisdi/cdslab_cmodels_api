from uuid import uuid1
from unittest import TestCase

from mongoengine import connect, disconnect

from src.models.db.model import (
    Model,
    StateVariable,
    Parameter
)
from src.interfaces.model import ModelInterface
from src.utils.encoder import BsonObject


class ModelInterfaceTestCase(TestCase):
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.model_id = uuid1()
        self.model_name = "test"

        self.parameter = [Parameter(
            label="test",
            representation="unittest",
            unit="unit",
            min_value=0.0,
            max_value=5.0
        )]
        
        self.state = [StateVariable(
            label="test",
            representation="unit",
            unit="unittest",
            can_fit=True
        )]

        Model(
            name=self.model_name,
            identifier=self.model_id,
            state_variables=self.state,
            parameters=self.parameter
        ).save()
    
    def tearDown(self):
        disconnect()

    def test_find_one_by_name(self):
        model = ModelInterface.find_one_by_name(
            model_name=self.model_name
        )

        self.assertIsNotNone(model)
        self.assertEqual(model.name, self.model_name)
    
    def test_find_one_by_name_not_found(self):
        model = ModelInterface.find_one_by_name(
            model_name=""
        )
        
        self.assertIsNone(model)

    def test_find_one_by_uuid(self):
        model = ModelInterface.find_one_by_uuid(
            uuid=self.model_id
        )

        self.assertIsNotNone(model)
        self.assertIsInstance(model,Model)
        self.assertEqual(model.name, self.model_name)
    
    def test_find_one_by_uuid_not_found(self):
        model = ModelInterface.find_one_by_uuid(
            uuid=uuid1()
        )

        self.assertIsNone(model)
        
    def test_find_all(self):
        model = ModelInterface.find_all()

        models = BsonObject.dict(model)

        self.assertTrue(len(models) > 0)
        self.assertIsNotNone(model)
    
