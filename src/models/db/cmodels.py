from pydantic import BaseModel
from datetime import datetime


class CModelInDB(BaseModel):

    inserted_at: datetime
    updated_at: datetime
