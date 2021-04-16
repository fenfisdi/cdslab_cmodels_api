from pydantic import BaseModel
from datetime import datetime

from src.models.routers.cmodel import AllCModels
from src.utils.date_time import DateTime


class CModelInDB(BaseModel):

    inserted_at: datetime
    updated_at: datetime
