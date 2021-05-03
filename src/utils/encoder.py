from datetime import datetime
from json import JSONEncoder
from typing import Union
from uuid import UUID

from bson import ObjectId
from mongoengine import Document, QuerySet
from ujson import loads


class BsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        return JSONEncoder.default(self, o)


class BsonObject:

    @classmethod
    def dict(cls, document: Union[Document, Document]):
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
        invalid_keys = {
            "_id", "_cls", "inserted_at", "updated_at", "is_deleted"
        }

        for k in data.copy().keys():
            if k in invalid_keys:
                del data[k]
        return data
