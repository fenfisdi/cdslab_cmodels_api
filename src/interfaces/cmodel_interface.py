from src.db.mongo import get_db
from src.config import db_config


def cmodel_collection():
    db_connection, db = get_db()
    cmodels_coll = db[db_config['CMODELS_COLL']]
    return db_connection, cmodels_coll


class CmodelInterface:

    @staticmethod
    def insert_cmodels_documents(models_list):
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
        db_connection, cmodels_coll = cmodel_collection()
        with db_connection as client:
            if cmodels_coll.find_one({'_id': {"$exists": True}}):
                return "models already exists"
            return [cmodels_coll.insert_one(model) for model in models_list][0]
