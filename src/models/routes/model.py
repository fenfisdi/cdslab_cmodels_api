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
    can_fit: bool = Field(True)


class NewModel(BaseModel):
    name: str = Field(..., max_length=50)
    state_variables: List[StateVariable] = Field(...)
    parameters: List[Parameter] = Field(...)


class UpdateModel(NewModel):
    name: str = Field(None, max_length=50)
    state_variables: List[StateVariable] = Field(None)
    parameters: List[Parameter] = Field(None)
