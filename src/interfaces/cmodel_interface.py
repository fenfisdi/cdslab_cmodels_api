from src.db.mongo import get_collection


class CmodelInterface:

    db_connection, cmodels_coll = get_collection()

    @staticmethod
    def insert_cmodel(model):
        """Check if the default compartmental models exists.

        Parameters
        ----------
        model
            The compartmental models that will be save in the database

        Return
        ----------
        model: pymongo object
        """
        with CmodelInterface.db_connection:
            return CmodelInterface.cmodels_coll.insert_one(model)

    @staticmethod
    def read_model(query):
        """Search for a specific model inside the database.

        Parameters
        ----------
        query: dict
            Key pair associated to the user

        Return
        ----------
        model: pymongo object
            Object containing the results of the search
        """
        with CmodelInterface.db_connection:
            return CmodelInterface.cmodels_coll.find_one(query)

    @staticmethod
    def update_model(query, model):
        """Update model's status to active after verification

        Parameters
        ----------
        data: dict
            Updated model parameters

        query: str
            Key pair associated to the user

        Return
        ----------
        False:
            * If model has no information
            * If is not possible to update the model's status
            * If the id doesn't match the one associated to the data parameter
        True:
            If the model has valid data and its status can be updated
        """

        with CmodelInterface.db_connection:
            if not bool(model):
                return False
            cmodel = CmodelInterface.cmodels_coll.find_one(query)
            if cmodel:
                update_model = CmodelInterface.cmodels_coll.update_one(
                    query,
                    {"$set": model},
                )
                if update_model:
                    return True
            return False

    @staticmethod
    def delete_model(query):
        with CmodelInterface.db_connection:
            return CmodelInterface.cmodels_coll.delete_one(query)
