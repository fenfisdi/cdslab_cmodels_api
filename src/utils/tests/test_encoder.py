from datetime import datetime
from json import loads
from unittest import TestCase

from bson import ObjectId
from mongoengine import StringField, IntField, Document, DateTimeField

from src.utils.encoder import BsonEncoder, BsonObject


class BsonEncoderTestCase(TestCase):

    def test_bson_encoder_ok(self):
        data = {
            'bson_id': ObjectId(),
            'int': 1,
            'str': 'any_word',
            'datetime': datetime(2021, 2, 3)
        }
        result = BsonEncoder().encode(data)

        self.assertIsInstance(result, str)
        dict_result = loads(result)
        self.assertIsInstance(dict_result.get('datetime'), str)
        self.assertIsInstance(dict_result.get('bson_id'), str)


class BsonObjectTestCase(TestCase):

    def test_bson_dict(self):
        class Example(Document):
            inserted_at = DateTimeField()
            name = StringField()
            age = IntField()

        data = Example(
            inserted_at=datetime.now(),
            name='name',
            age=20
        )

        result = BsonObject.dict(data)

        mock_result = {
            'name': 'name',
            'age': 20,
        }
        self.assertIsInstance(result, dict)
        self.assertEqual(result['name'], mock_result['name'])
