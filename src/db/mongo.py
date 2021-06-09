from os import environ

from mongoengine import connect

from src.utils.patterns import Singleton


class MongoEngine(metaclass=Singleton):
    """
        Class that handle Mongodb connection
    """
    def __init__(self):
        """
            Class constructor
        """
        self.mongo_uri = environ.get('MONGO_URI')

    def get_connection(self):
        """
        Get mongo URL
        """
        return connect(host=self.mongo_uri)
