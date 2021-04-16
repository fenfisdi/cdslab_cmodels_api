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

        with CmodelInterface.db_connection as client:
            CmodelInterface.cmodels_coll.insert_one(model)

    def read_model(query):
        """
            Docstring
        """
        with CmodelInterface.db_connection as client:

            return CmodelInterface.cmodels_coll.find_one(query)

    def update_model(colection_name, model):
        """
            Docstring
        """

        with CmodelInterface.db_connection as client:

            CmodelInterface.cmodels_coll.update_one(colection_name, model)
