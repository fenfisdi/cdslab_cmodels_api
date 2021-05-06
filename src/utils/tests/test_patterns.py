from unittest import TestCase

from src.utils.patterns import Singleton


class SingletonTestCase(TestCase):

    def test_same_class(self):
        class AnyCLass(metaclass=Singleton):
            pass

        a = AnyCLass()
        b = AnyCLass()

        self.assertIsNotNone(a)
        self.assertIsNotNone(a)
        self.assertEqual(id(a), id(b))
