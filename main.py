import uvicorn
from cmodels_api.config import settings

if __name__ == '__main__':
    uvicorn.run(
        "cmodels_api.api:app",
        host=settings['HOST'],
        port=int(settings['PORT']),
        reload=True,
        debug=True, workers=1
    )
