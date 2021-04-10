from enum import Enum
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, validator

from src.config import settings


class SimulationType(str, Enum):
    optimize = 'Optimize parameters'
    fixed = 'Fixed parameters'


class SimulationConfig(BaseModel):
    user_id: ObjectId
    model_id: ObjectId
    name: str
    creation_date: datetime = datetime.now()
    simulation_type: SimulationType

