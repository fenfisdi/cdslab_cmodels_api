import uvicorn
from src.config import settings
from src.interfaces.cmodel_interface import CmodelInterface
from src.models.cmodel import AllCModels


if __name__ == '__main__':
    CmodelInterface.created_cmodel_collection(AllCModels)
    uvicorn.run(
        "src.api:app",
        host=settings['HOST'],
        port=int(settings['PORT']),
        reload=True,
        debug=True,
        workers=1
    )
