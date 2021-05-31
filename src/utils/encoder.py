from datetime import datetime
from json import JSONEncoder
from typing import Union
from uuid import UUID

from bson import DBRef, ObjectId
from mongoengine import Document, QuerySet
from ujson import loads


class BsonEncoder(JSONEncoder):
    '''
        Class that allows conversion to JSON
    '''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, DBRef):
            return o.id
        return JSONEncoder.default(self, o)


class BsonObject:
    '''
        Transform a mongodb document into a dictionary
    '''
    @classmethod
    def dict(cls, document: Union[Document, Document]):
        '''
            Creates a python dictionary based in a mongodb document
        Parameters:
            document (Document): Mongodb document to transform
        Return:
            dict: Dictionary with keys and values from mongodb document
        '''
        if isinstance(document, QuerySet):
            document = [value.to_mongo() for value in document]
            raw = BsonEncoder().encode(document)
        else:
            raw = BsonEncoder().encode(document.to_mongo())
        document_dict = loads(raw)

        if isinstance(document_dict, dict):
            return cls.__filter_keys(document_dict)
        if isinstance(document_dict, list):
            return [cls.__filter_keys(document) for document in document_dict]
        raise TypeError('Invalid Type')

    @classmethod
    def __filter_keys(cls, data: dict) -> dict:
        '''
            Remove sensitive data from the dictionary
        Parameters:
            data (dict): Dictionary with data to filter
        Return:
            dict: Dictionary without sensitive keys
        '''
        invalid_keys = {
            "_id", "_cls", "updated_at", "is_deleted"
        }

        for k in data.copy().keys():
            if k in invalid_keys:
                del data[k]
        return data
