from fastapi import APIRouter, BackgroundTasks
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from src.interfaces import INSInterface
from src.use_cases import CreatePredefinedINS
from src.utils.encoder import BsonObject
from src.utils.messages import INSMessage
from src.utils.response import UJSONResponse

ins_routes = APIRouter(prefix='/ins')


@ins_routes.get('/variables')
def list_ins_variables(background_task: BackgroundTasks):
    background_task.add_task(CreatePredefinedINS.handle)

    variables = INSInterface.find_all()
    if not variables:
        return UJSONResponse(INSMessage.not_found, HTTP_400_BAD_REQUEST)
    return UJSONResponse(
        INSMessage.found,
        HTTP_200_OK,
        BsonObject.dict(variables)
    )
