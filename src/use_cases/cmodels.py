from src.db.mongo import get_collection
from src.interfaces.cmodels import CModelsInterface


class CmodelUseCases:
    db_connection, cmodels_coll = get_collection()
    cmodels_interface = CModelsInterface(db_connection, cmodels_coll)

    @staticmethod
    def update_cmodels_collection(
        cmodels_interface: CModelsInterface = cmodels_interface
    ):
        cmodels_interface.insert_all_cmodel_documents()
