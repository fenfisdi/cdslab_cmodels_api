from datetime import datetime

from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient

from src.models.db.cmodels import (
    CompartmentalModelBase,
    CompartmentalModelEnum
)
from src.models.db.cmodels import CompartmentalModel
from src.interfaces.crud import MongoCRUD


class CModelsInterface:
    def __init__(
        self,
        db_connection: MongoClient,
        collection: Collection
    ) -> None:
        self.crud = MongoCRUD(db_connection, collection)

    def insert_one_cmodel_document(self, model: CompartmentalModelBase):

        id_dict = {'_id': model.name.encode('utf-8').hex()}

        cmodel_document = CompartmentalModel(
            id=id_dict['_id'],
            inserted_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            **model.dict()
        ).dict(by_alias=True)

        existent_model = self.crud.read(id_dict)

        if existent_model:
            pruned_existent_model = CModelsInterface._prune_db_document(
                existent_model
            )
            if pruned_existent_model == model.dict(by_alias=True):
                # TODO: log cmodel exists
                print(f'Cmodel exists: {model.name}')
            else:
                cmodel_document.pop('inserted_at')
                self.crud.update(
                    id_dict,
                    cmodel_document
                )
                # TODO log updated cmodel
                print(f'Updated cmodel: {model.name}')
        else:
            self.crud.insert(cmodel_document)
            # TODO: log created cmodel
            print(f'Created cmodel: {model.name}')

    def insert_all_cmodel_documents(self, ):
        for model in CompartmentalModelEnum.values():
            self.insert_one_cmodel_document(model)

    @staticmethod
    def _prune_db_document(model_in_db: dict) -> dict:
        model_in_db.pop('_id')
        model_in_db.pop('inserted_at')
        model_in_db.pop('updated_at')
        return model_in_db
