from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import ModelInterface, SimulationInterface
from src.models.db import Simulation
from src.models.routes import NewSimulation, UpdateSimulation
from src.use_cases.identifier import IdentifierUseCase
from src.use_cases.security import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import ModelMessage, SimulationMessage
from src.utils.response import UJSONResponse

simulation_routes = APIRouter(tags=['Simulation'])


@simulation_routes.post('/simulation')
def create_simulation(
        simulation: NewSimulation,
        user=Depends(SecurityUseCase.validate)
):
    """
    Create custom simulation of user according with definite model.

    \f
    :param simulation: simulation to create from a model.
    :param user: user information.
    """
    simulation_found = SimulationInterface.find_one_by_name(
        user,
        simulation.name
    )
    if simulation_found:
        return UJSONResponse(SimulationMessage.exist, HTTP_400_BAD_REQUEST)

    model = ModelInterface.find_one_by_uuid(simulation.model_id)
    if not model:
        return UJSONResponse(ModelMessage.not_found, HTTP_404_NOT_FOUND)

    simulation_data = simulation.dict(exclude={'model_id'})
    simulation_data.update(
        {
            'model': model,
            'user': user,
            'identifier': IdentifierUseCase.create_identifier(),
        }
    )
    simulation = Simulation(**simulation_data)

    try:
        simulation.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(
        SimulationMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(simulation)
    )


@simulation_routes.get('/simulation/{uuid}')
def find_simulation(uuid: UUID, user=Depends(SecurityUseCase.validate)):
    """
    Find user simulation with its uuid.

    \f
    :param uuid: uuid from specific simulation.
    :param user: user information.
    """
    simulation = SimulationInterface.find_one_by_uuid(user, uuid)
    if not simulation:
        return UJSONResponse(SimulationMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        SimulationMessage.found,
        HTTP_200_OK,
        BsonObject.dict(simulation)
    )


@simulation_routes.get('/simulation')
def list_simulation(user=Depends(SecurityUseCase.validate)):
    """
    List all user simulation created from a specific model.

    \f
    :param user: user information.
    """
    simulation = SimulationInterface.find_all(user)
    if not simulation:
        return UJSONResponse(SimulationMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        SimulationMessage.found,
        HTTP_200_OK,
        BsonObject.dict(simulation)
    )


@simulation_routes.put('/simulation/{uuid}')
def update_simulation(
        uuid: UUID,
        simulation: UpdateSimulation,
        user=Depends(SecurityUseCase.validate)
):
    """
    Update user simulation according with the input fields.

    \f
    :param uuid: model reference to update.
    :param simulation: simulation input data to update.
    :param user: user information.
    """
    simulation_found = SimulationInterface.find_one_by_uuid(user, uuid)
    if not simulation_found:
        return UJSONResponse(SimulationMessage.not_found, HTTP_404_NOT_FOUND)

    simulation_found.update(**simulation.dict())
    try:
        simulation_found.save()
        simulation_found.reload()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(
        SimulationMessage.updated,
        HTTP_200_OK,
        BsonObject.dict(simulation_found)
    )


@simulation_routes.delete('/simulation/{uuid}')
def delete_simulation(uuid: UUID, user=Depends(SecurityUseCase.validate)):
    """

    :param uuid:
    :param user:
    """
    simulation_found = SimulationInterface.find_one_by_uuid(user, uuid)
    if not simulation_found:
        return UJSONResponse(SimulationMessage.not_found, HTTP_404_NOT_FOUND)

    simulation_found.is_deleted = True
    try:
        simulation_found.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
    return UJSONResponse(SimulationMessage.deleted, HTTP_200_OK)
