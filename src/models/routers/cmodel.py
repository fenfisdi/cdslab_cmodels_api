from enum import Enum
from typing import Dict, List
from datetime import datetime
from pydantic import BaseModel


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


class CompartmentalModel(Enum):
    """Compartmental Models' Data.

    Each element of this ``Enum`` class contains all the essential information
    on the corresponding Compartmental Model. Each element is a
    :class:``CompartmentalModelBase`` object
    """
    sir = CompartmentalModelBase(
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

    seir = CompartmentalModelBase(
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

    seirv = CompartmentalModelBase(
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
        },
    )


class CModel(BaseModel):
    model: CompartmentalModel


class AllCModels(BaseModel):
    models: List[CompartmentalModel] = [
        model.value for model in CompartmentalModel
    ]


class CModelInDB(BaseModel):

    inserted_at: datetime
    updated_at: datetime
