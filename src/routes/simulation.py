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
from src.models.routes import NewSimulation
from src.use_cases.security import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import ModelMessage, SimulationMessage
from src.utils.response import UJSONResponse

simulation_routes = APIRouter(tags=['Simulation'])


@simulation_routes.post('/simulation')
def create_simulation(simulation: NewSimulation,
                      user=Depends(SecurityUseCase.validate)):
    simulation_found = SimulationInterface.find_one_by_name(user,
                                                            simulation.name)
    if simulation_found:
        return UJSONResponse(SimulationMessage.exist, HTTP_400_BAD_REQUEST)

    model = ModelInterface.find_one_by_uuid(simulation.model_id)
    if not model:
        return UJSONResponse(ModelMessage.not_found, HTTP_404_NOT_FOUND)

    simulation_data = simulation.dict(exclude={'model_id'})
    simulation_data.update(
        {
            'model': model,
            'user': user
        }
    )
    simulation = Simulation(**simulation_data)

    try:
        simulation.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(SimulationMessage.created, HTTP_201_CREATED,
                         BsonObject.dict(simulation))


@simulation_routes.get('/simulation/{uuid}')
def create_simulation(uuid: UUID, user=Depends(SecurityUseCase.validate)):
    simulation = SimulationInterface.find_one_by_uuid(user, uuid)
    if not simulation:
        return UJSONResponse(SimulationMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(SimulationMessage.found, HTTP_200_OK,
                         BsonObject.dict(simulation))
