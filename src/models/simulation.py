from enum import Enum
from datetime import datetime

from bson.objectid import ObjectId
from pydantic import BaseModel


class SimulationType(str, Enum):
    optimize = 'Optimize parameters'
    fixed = 'Fixed parameters'


class SimulationConfig(BaseModel):
    user_id: ObjectId
    model_id: ObjectId
    name: str
    creation_date: datetime = datetime.now()
    simulation_type: SimulationType
