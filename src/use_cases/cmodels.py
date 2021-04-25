from src.db.mongo import MongoClientSingleton
from src.interfaces.cmodels import CModelsInterface


class CmodelUseCases:

    def __init__(
        self,
        mongo_singleton: MongoClientSingleton
    ) -> None:
        self.mongo_singleton = mongo_singleton
        self.cmodels_interface = CModelsInterface(self.mongo_singleton)

    def update_cmodels_collection(self) -> None:
        self.cmodels_interface.insert_all_cmodel_documents()
