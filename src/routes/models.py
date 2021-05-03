from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

from src.models.db.model import Model
from src.models.routes.model import NewModel
from src.utils.encoder import BsonObject
from src.utils.messages import ModelMessage
from src.utils.response import UJSONResponse

model_routes = APIRouter(tags=['Models'])


@model_routes.post('/model')
def create_model(model: NewModel):
    model = Model(**model.dict())
    try:
        model.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
    return UJSONResponse(
        ModelMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(model)
    )


@model_routes.get('/model')
async def list_models():
    return UJSONResponse(ModelMessage.found_all, HTTP_200_OK)
