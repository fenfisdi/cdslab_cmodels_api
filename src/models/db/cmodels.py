from pydantic import BaseModel
from datetime import datetime

from src.models.routers.cmodel import AllCModels


class CModelInDB(BaseModel):

    inserted_at: datetime
    updated_at: datetime
