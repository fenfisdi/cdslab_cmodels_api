from typing import Any, Union

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
            return self.collection.insert_one(document)

    def read(self, query: dict) -> Union[Any, None]:
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
            return self.collection.find_one(query)

    def update(self, query: dict, new_data: dict) -> bool:
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

        with self.db_connection:
            if not query:
                return False
            cmodel = self.collection.find_one(query)
            if cmodel:
                update_model = self.collection.update_one(
                    query,
                    {"$set": new_data},
                )
                if update_model:
                    return True
            return False

    def delete(self, query):
        with self.db_connection:
            return self.collection.delete_one(query)
