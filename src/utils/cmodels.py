from datetime import datetime

from src.db.mongo import get_collection
from src.models.db.cmodels import (
    CompartmentalModelBase,
    CompartmentalModelEnum
)
from src.models.db.cmodels import CompartmentalModel
from src.interfaces.crud import MongoCRUD
from src.use_cases.cmodels import CmodelUseCases


def insert_cmodels_document():

    for model in CompartmentalModelEnum:
        model: CompartmentalModelBase = model.value

        cmodel_document = CompartmentalModel(
            id=model.name.encode('utf-8').hex(),
            inserted_at=datetime.now(),
            updated_at=datetime.now(),
            **model.dict()
        ).dict(by_alias=True)

        cmodels_crud = MongoCRUD(*get_collection())

        existent_model = cmodels_crud.read({"name": model.name})
        if existent_model:
            pruned_existent_model = \
                CmodelUseCases.model_information_in_db_to_compare(
                    existent_model
                )
            if pruned_existent_model == model.dict():
                # TODO: log cmodel exists
                ...
            else:
                cmodel_document.pop('inserted_at')
                cmodels_crud.update(cmodel_document)
                # TODO log updated cmodel
        else:
            cmodels_crud.insert(cmodel_document)
            # TODO: log created cmodel
