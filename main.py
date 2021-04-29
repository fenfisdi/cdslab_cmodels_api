from src.db.mongo import MongoClientSingleton
import uvicorn

from src.api import app
from src.config import settings
from src.use_cases.cmodels import CmodelUseCases


mongo_singleton = MongoClientSingleton()
CmodelUseCases(mongo_singleton).update_cmodels_collection()

__all__ = ['app']


if __name__ == '__main__':
    uvicorn.run(
        "src.api:app",
        host=settings.get('HOST'),
        port=int(settings['PORT']),
        reload=True,
        debug=True,
        workers=1
    )
