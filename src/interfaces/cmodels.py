from datetime import datetime

from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient

from src.models.db.cmodels import (
    CompartmentalModel,
    CompartmentalModelEnum
)
from src.interfaces.crud import MongoCRUD


class CModelsInterface:

    def __init__(
        self,
        db_connection: MongoClient,
        collection: Collection
    ) -> None:
        self.crud = MongoCRUD(db_connection, collection)

    def insert_one_cmodel_document(self, model: CompartmentalModel):

        cmodel_document = model.dict(by_alias=True)

        existent_model = self.crud.read(model.id)

        if existent_model:
            pruned_existent_model = CModelsInterface._prune_db_document(
                existent_model
            )
            pruned_current_model = CModelsInterface._prune_db_document(
                cmodel_document
            )
            if pruned_existent_model == pruned_current_model:
                # TODO: log cmodel exists f'Cmodel exists: {model.name}'
                return existent_model
            else:
                model.updated_at = datetime.utcnow()
                updated_model = self.crud.update(
                    model.id,
                    model.dict(by_alias=True)
                )
                # TODO log updated cmodel f'Updated cmodel: {model.name}'
                return updated_model
        else:
            model_inserted = self.crud.insert(cmodel_document)
            # TODO: log created cmodel f'Created cmodel: {model.name}'
            return model_inserted

    def insert_all_cmodel_documents(self):
        return [self.insert_one_cmodel_document(model) for model in CompartmentalModelEnum.values()]

    @staticmethod
    def _prune_db_document(model_in_db: dict) -> dict:
        if model_in_db:
            model_in_db.pop('inserted_at')
            model_in_db.pop('updated_at')
            return model_in_db
