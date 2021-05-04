from datetime import datetime
from typing import Tuple
from uuid import UUID

from pydantic import BaseModel, Field


class UpdateSimulation(BaseModel):
    name: str = Field(None)
    optimize_parameters: bool = Field(None)
    interval_date: Tuple[datetime, datetime] = Field(None)
    parameters_limits: dict = Field(None)
    state_variables_init_vals: dict = Field(None)
    state_variable_to_fit: dict = Field(None)


class NewSimulation(UpdateSimulation):
    model_id: UUID = Field(...)
