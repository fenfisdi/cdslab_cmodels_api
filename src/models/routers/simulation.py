from enum import Enum
from datetime import datetime

from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return v

class SimulationType(str, Enum):
    optimize = 'Optimize parameters'
    fixed = 'Fixed parameters'


class SimulationConfig(BaseModel):
    user_id: PydanticObjectId
    model_id: str
    name: str
    creation_date: datetime = datetime.now()
    simulation_type: SimulationType
