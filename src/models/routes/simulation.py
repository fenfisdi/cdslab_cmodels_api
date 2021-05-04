from datetime import datetime
from typing import Tuple
from uuid import UUID

from pydantic import BaseModel, Field


class NewSimulation(BaseModel):
    model_id: UUID = Field(...)
    name: str = Field(...)
    optimize_parameters: bool = Field(...)
    interval_date: Tuple[datetime, datetime] = Field(...)
    parameters_limits: dict = Field(...)
    state_variables_init_vals: dict = Field(...)
    state_variable_to_fit: dict = Field(...)
