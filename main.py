import uvicorn
from datetime import datetime

from src.config import settings
from src.interfaces.cmodel_interface import CmodelInterface
from src.models.routers.cmodel import AllCModels
from src.models.db.cmodels import CModelInDB


def insert_cmodels_document():
    for model in AllCModels().models:
        cmodel_db_base = dict({'_id': model.name.encode('utf-8').hex()}, **CModelInDB(
            inserted_at=datetime.now(),
            updated_at=datetime.now()).dict())
        model_in_db = dict(cmodel_db_base, **model.dict())
        verify_model = CmodelInterface.read_model({"name": model.name})

        if verify_model:
            if (dict(verify_model) == dict(model_in_db)):
                print(f'{"model: "}{model.name}{"Already exist"}')
            return CmodelInterface.update_model(
                {'name': model.name}, {"$set": model_in_db})
        return CmodelInterface.insert_cmodel(model_in_db)


if __name__ == '__main__':

    insert_cmodels_document()
    uvicorn.run(
        "src.api:app",
        host=settings['HOST'],
        port=int(settings['PORT']),
        reload=True,
        debug=True,
        workers=1
    )
