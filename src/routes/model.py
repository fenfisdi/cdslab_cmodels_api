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
from src.use_cases.identifier import IdentifierUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import ModelMessage
from src.utils.response import UJSONResponse

model_routes = APIRouter(tags=['Model'])


@model_routes.post('/model')
def create_model(model: NewModel):
    """
    Create model to storage in database for simulations.

    \f
    :param model: model information to save.
    """
    model_found = ModelInterface.find_one_by_name(model.name)
    if model_found:
        return UJSONResponse('Exist', HTTP_400_BAD_REQUEST)

    model = Model(
        **model.dict(),
        identifier=IdentifierUseCase.create_identifier()
    )
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
    """
    Find model by uuid

    \f
    :param uuid: model identifier to find.
    """
    model = ModelInterface.find_one_by_uuid(uuid)
    if not model:
        return UJSONResponse(ModelMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        ModelMessage.found,
        HTTP_200_OK,
        BsonObject.dict(model)
    )


@model_routes.get('/model')
def list_model():
    """
    List all models in database
    """
    models = ModelInterface.find_all()
    if not models:
        return UJSONResponse(ModelMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        ModelMessage.found_all,
        HTTP_200_OK,
        BsonObject.dict(models)
    )
