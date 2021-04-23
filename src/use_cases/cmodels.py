from src.db.mongo import get_collection
from src.interfaces.cmodels import CModelsInterface


class CmodelUseCases:

    @staticmethod
    def update_cmodels_collection():
        db_connection, cmodels_coll = get_collection()
        cmodels_interface = CModelsInterface(db_connection, cmodels_coll)
        cmodels_interface.insert_all_cmodel_documents()
