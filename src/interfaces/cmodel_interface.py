from src.db.mongo import get_db_connection


def model_db():
    return get_db_connection()['cmodels']


class CmodelInterface:

    @staticmethod
    def created_cmodel_collection(AllCModels):
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
        if model_db().find_one({'_id': {"$exists": True}}):
            return print("models Already exist")
        return [model_db().insert_one(model) for model in AllCModels().models]
