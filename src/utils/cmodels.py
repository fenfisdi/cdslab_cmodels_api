from datetime import datetime

from src.interfaces.crud import MongoCRUD
from src.models.routers.cmodel import AllCModels
from src.models.db.cmodels import CModelInDB
from src.use_cases.cmodels import CmodelUseCases


def insert_cmodels_document():

    for model in AllCModels().models:
        cmodel_db_base = dict(CmodelUseCases.create_id_cmodel(model.name),
                              **CModelInDB(inserted_at=datetime.now(),
                                           updated_at=datetime.now()).dict())
        model_in_db = dict(cmodel_db_base, **model.dict())
        find_model = MongoCRUD.read_model({"name": model.name})
        if find_model:
            model_to_compare = CmodelUseCases.model_information_in_db_to_compare(
                find_model)
            if (dict(model_to_compare) == dict(model)):
                print(f'{"model: "}{model.name}{" Already exist"}')
            else:
                model_in_db.pop('inserted_at')
                MongoCRUD.update_model(
                    {'name': model.name}, model_in_db)
                print(f'{"model: "}{model.name}{" Updated"}')
        else:
            MongoCRUD.insert_cmodel(model_in_db)
