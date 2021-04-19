from src.db.mongo import get_db
from src.config import db_config


def cmodel_collection():
    db_connection, db = get_db()
    cmodels_coll = db[db_config['CMODELS_COLL']]
    return db_connection, cmodels_coll


class CmodelInterface:

    db_connection, cmodels_coll = cmodel_collection()

    @staticmethod
    def insert_cmodel(model):
        """
            Check if the default compartmental models exists
            and if not, create them within the cmodels collection

            Parameters
            ----------
            AllCmodels: dict
                The compartmental models that will be save in the database

            Return
            ----------
            model: pymongo object
        """

        with CmodelInterface.db_connection:
            return CmodelInterface.cmodels_coll.insert_one(model)

    def read_model(query):
        """
            Search for a specific model inside the database

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

    def update_model(query, model):
        """
            Update model's status to active after verification

            Parameters
            ----------
            data: dict
                Updated model parameters

            query: str
                Key pair associated to the user

            Return
            ----------
            False:
                If model has no information
            False:
                If is not possible to update the model's status
            False:
                If the id doesn't match the one associated to the data parameter
            True:
                If the model has valid data and its status can be updated
        """

        with CmodelInterface.db_connection:

            if not bool(model):
                return False
            cmodel = CmodelInterface.cmodels_coll.find_one(query)
            print(cmodel)
            if cmodel:
                update_model = CmodelInterface.cmodels_coll.update_one(query, {
                                                                       "$set": model})
                if update_model:
                    return True
            return False

    def delete_model(query):

        with CmodelInterface.db_connection:

            return CmodelInterface.cmodels_coll.delete_one(query)
