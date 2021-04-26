from bson.objectid import ObjectId

from src.models.db.simulations import SimulationConfigDB
from tests.models.routers.test_simulations import sim_config


def test_SimulationConfig():
    SimulationConfigDB(
        **{
            **sim_config,
            **{
                'id': ObjectId(),
                'attached_time_series': None,
            }
        }
    )
