from typing import List

from pydantic import BaseModel, Field


class Parameter(BaseModel):
    label: str = Field(...)
    representation: str = Field(...)
    unit: str = Field(...)
    min_value: float = Field(...)
    max_value: float = Field(...)


class StateVariable(BaseModel):
    label: str = Field(...)
    representation: str = Field(...)
    unit: str = Field(...)


class NewModel(BaseModel):
    name: str = Field(..., max_length=50)
    state_variables: List[StateVariable] = Field(...)
    parameters: List[Parameter] = Field(...)
