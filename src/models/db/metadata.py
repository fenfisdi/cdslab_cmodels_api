from datetime import datetime

from pydantic import BaseModel, Field

from src.models.general_config import PydanticObjectId, GeneralConfig


class MetadataBaseDoc(BaseModel):
    id: PydanticObjectId = Field(..., alias='_id')
    inserted_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config(GeneralConfig):
        ...
