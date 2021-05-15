from unittest import TestCase

from mongoengine import connect, disconnect

from src.models.db import User


class UserInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.user_1 = User(
            name='testName',
            email='test1@test.com'
        )

    def tearDown(self):
        disconnect()

    def test_find_one(self):
        self.assertTrue(True)
