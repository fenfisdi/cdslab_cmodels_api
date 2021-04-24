from src.db.mongo import MongoClientSingleton
from src.interfaces.cmodels import CModelsInterface


class CmodelUseCases:

    def __init__(
        self,
        mongo_singleton: MongoClientSingleton = MongoClientSingleton()
    ) -> None:
        self.mongo_singleton = mongo_singleton
        self.db_connection, self.cmodels_coll = self.mongo_singleton.get_collection()
        self.cmodels_interface = CModelsInterface(self.db_connection, self.cmodels_coll)

    def update_cmodels_collection(self) -> None:
        self.cmodels_interface.insert_all_cmodel_documents()
