import uvicorn

from src.config import settings
from src.utils.cmodels import insert_cmodels_document

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
