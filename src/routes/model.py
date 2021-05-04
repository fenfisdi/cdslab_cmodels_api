from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import ModelInterface
from src.models.db import Model
from src.models.routes.model import NewModel
from src.utils.encoder import BsonObject
from src.utils.messages import ModelMessage
from src.utils.response import UJSONResponse

model_routes = APIRouter(tags=['Model'])


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


@model_routes.get('/model/{uuid}')
def find_model(uuid: str):
    model = ModelInterface.find_one_by_uuid(uuid)
    if not model:
        return UJSONResponse(ModelMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        ModelMessage.found,
        HTTP_200_OK,
        BsonObject.dict(model)
    )


@model_routes.get('/model')
def list_models():
    models = ModelInterface.find_all()
    if not models:
        return UJSONResponse(ModelMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        ModelMessage.found_all,
        HTTP_200_OK,
        BsonObject.dict(models)
    )
