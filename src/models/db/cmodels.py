from datetime import datetime

from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, List


class CompartmentalModelBase(BaseModel):
    """Base Model for Compartmental Models
    """
    name: str
    """Name of the compartmental model"""
    state_variables: List[str]
    """Name of state variables of corresponding model"""
    state_variables_units: Dict[str, str]
    """Units of each state variable. The keys are the 'state_variables' array
    elements
    """
    parameters: List[str]
    """Parameters of the corresponding model"""
    parameters_units: Dict[str, str]
    """Units of each parameter. The keys are the 'parameters' array elements"""


class CompartmentalModel(CompartmentalModelBase):
    id: str = Field(..., alias='_id')
    inserted_at: datetime
    updated_at: datetime

    class Config:
        allow_population_by_field_name = True


class CompartmentalModelEnum(Enum):
    """Compartmental Models' Data.

    Each element of this ``Enum`` class contains all the essential information
    on the corresponding Compartmental Model. Each element is a
    :class:``CompartmentalModelBase`` object
    """
    sir: CompartmentalModelBase = CompartmentalModelBase(
        name='SIR',
        state_variables=['S', 'I', 'R'],
        state_variables_units={
            'S': 'persons',
            'I': 'persons',
            'R': 'persons',
        },
        parameters=['a', 'b'],
        parameters_units={
            'a': 'units of a',
            'b': 'units of b',
        },
    )

    seir: CompartmentalModelBase = CompartmentalModelBase(
        name='SEIR',
        state_variables=['S', 'E', 'I', 'R'],
        state_variables_units={
            'S': 'persons',
            'E': 'persons',
            'I': 'persons',
            'R': 'persons',
        },
        parameters=['a', 'b'],
        parameters_units={
            'a': 'units of a',
            'b': 'units of b',
        },
    )

    seirv: CompartmentalModelBase = CompartmentalModelBase(
        name='SEIRV',
        state_variables=['S', 'E', 'I', 'R', 'V'],
        state_variables_units={
            'S': 'persons',
            'E': 'persons',
            'I': 'persons',
            'R': 'persons',
            'V': 'persons',
        },
        parameters=['a', 'b'],
        parameters_units={
            'a': 'units of a',
            'b': 'units of b',
            'c': 'units_test'
        },
    )


class CModel(BaseModel):
    model: CompartmentalModelEnum


class AllCModels(BaseModel):
    models: List[CompartmentalModelEnum] = [
        model.value for model in CompartmentalModelEnum
    ]
