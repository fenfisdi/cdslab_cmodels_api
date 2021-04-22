import uvicorn

from src.config import settings
from src.use_cases.cmodels import CmodelUseCases


if __name__ == '__main__':
    CmodelUseCases.update_cmodels_collection()
    uvicorn.run(
        "src.api:app",
        host=settings['HOST'],
        port=int(settings['PORT']),
        reload=True,
        debug=True,
        workers=1
    )
