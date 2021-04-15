import uvicorn
from src.config import settings
from src.interfaces.cmodel_interface import CmodelInterface
from src.models.cmodel import AllCModels


if __name__ == '__main__':
    CmodelInterface.insert_cmodels_documents(AllCModels().models)
    uvicorn.run(
        "src.api:app",
        host=settings['HOST'],
        port=int(settings['PORT']),
        reload=True,
        debug=True,
        workers=1
    )
