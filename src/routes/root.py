from fastapi import APIRouter
from fastapi import Query
from starlette.status import HTTP_200_OK

from src.interfaces.simulation import RootSimulationInterface
from src.utils.encoder import BsonObject
from src.utils.messages import SimulationMessage
from src.utils.response import UJSONResponse

root_routes = APIRouter(prefix="/root", tags=['Root'], include_in_schema=False)


@root_routes.get('/simulation/expired')
def list_simulation_expired(to_expire: int = Query(-30, lt=0)):
    '''
        Check expired simulations
    Parameter:
        to_expire (int): expiration days
    Return:
        UJSONResponse: API response with info request 
    '''
    data = RootSimulationInterface.find_all_expired(to_expire)

    return UJSONResponse(
        SimulationMessage.found,
        HTTP_200_OK,
        BsonObject.dict(data)
    )
