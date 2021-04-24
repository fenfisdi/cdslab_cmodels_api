from typing import Any, Union
from bson.objectid import ObjectId

from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient


class MongoCRUD:
    def __init__(
        self,
        db_connection: MongoClient,
        collection: Collection
    ) -> None:
        self.db_connection = db_connection
        self.collection = collection

    def insert(self, document: dict):
        """
        Parameters
        ----------
        model
            The compartmental models that will be save in the database

        Return
        ----------
        model: pymongo object
        """
        with self.db_connection:
            try:
                document['_id']
            except KeyError:
                raise ValueError('self.insert(): document must have key "_id"')

            existent_document = self.collection.find_one(
                self._id_to_dict(document['_id'])
            )

            if existent_document:
                raise ValueError(
                    f'Document with _id={document["_id"]} already exists in'
                    'collection {self.collection}. if you want to change the'
                    'fields\' values please use self.update'
                )
                # TODO: log

            return self.collection.insert_one(document)

    def read(self, _id: ObjectId) -> Union[Any, None]:
        """Search for a specific model in ``self.collection``.

        Parameters
        ----------
        query
            Document's id. ``dict`` schema: ``{'_id': bson.ObjectID}``

        Return
        ----------
        model: pymongo object
            Object containing the results of the search
        """
        with self.db_connection:
            return self.collection.find_one(self._id_to_dict(_id))

    def update(self, _id: ObjectId, new_data: dict) -> bool:
        """Update document in ``self.collection``.

        Parameters
        ----------
        query
            Document's id. ``dict`` schema: ``{'_id': bson.ObjectID}``
        data
            Updated document fields

        Return
        ----------
        False:
            * If query has no information
            * If is not possible to update the document's status
            * If the query id doesn't match the one associated to ``new_data``
        True:
            If the model has valid data and its status can be updated
        """
        _id_dict = self._id_to_dict(_id)
        with self.db_connection:
            if not _id_dict:
                return False
            cmodel = self.collection.find_one(_id_dict)
            if cmodel:
                update_model = self.collection.update_one(
                    _id_dict,
                    {"$set": new_data},
                )
                if update_model:
                    return True
            return False

    def delete(self, _id: ObjectId):
        with self.db_connection:
            return self.collection.delete_one(self._id_to_dict(_id))

    def _id_to_dict(self, _id: ObjectId):
        return {'_id': _id} if _id else None
