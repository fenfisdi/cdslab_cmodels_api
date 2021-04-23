from enum import Enum
from datetime import datetime

from pydantic import BaseModel
from.base_model import PydanticObjectId


class SimulationType(str, Enum):
    optimize = 'Optimize parameters'
    fixed = 'Fixed parameters'


class SimulationConfig(BaseModel):
    user_id: PydanticObjectId
    model_id: str
    name: str
    creation_date: datetime = datetime.now()
    simulation_type: SimulationType
