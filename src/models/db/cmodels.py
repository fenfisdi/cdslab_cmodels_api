from enum import Enum
from src.models.general_config import GeneralConfig
from typing import Dict, List

from bson.objectid import ObjectId
from pydantic import BaseModel

from .metadata import MetadataBaseDoc


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


class CompartmentalModel(MetadataBaseDoc, CompartmentalModelBase):
    class Config(GeneralConfig):
        ...


class CompartmentalModelEnum(Enum):
    """Compartmental Models' Data.

    Each element of this ``Enum`` class contains all the essential information
    on the corresponding Compartmental Model. Each element is a
    :class:``CompartmentalModelBase`` object
    """
    sir: CompartmentalModelBase = CompartmentalModel(
        id=ObjectId('6083175ea91f5aacea234423'),
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

    seir: CompartmentalModelBase = CompartmentalModel(
        id=ObjectId('6083176ca91f5aacea234424'),
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

    seirv: CompartmentalModelBase = CompartmentalModel(
        id=ObjectId('608317d0a91f5aacea234426'),
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
            'c': 'units of c'
        },
    )

    @classmethod
    def values(cls) -> List[CompartmentalModel]:
        return [m.value for m in cls]


class CModel(BaseModel):
    model: CompartmentalModelEnum
