from enum import Enum
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator

from src.config import settings


class BaseCModel(Enum):
    """
        TODO: add docstring
    """
    pass


class SIR(BaseCModel):
    name = 'SIR'
    state_variables = ['S', 'I', 'R']
    state_variables_units = ['', '', '']
    parameters = ['a', 'b', 'c']
    parameters_units = ['', '', '']


class SEIR(BaseCModel):
    name = 'SEIR'
    state_variables = ['S', 'E', 'I', 'R']
    state_variables_units = ['', '', '']
    parameters = ['a', 'b', 'c', 'd']
    parameters_units = ['', '', '']


class SEIRV(BaseCModel):
    name = 'SEIRV'
    state_variables = ['S', 'E', 'I', 'R', 'V']
    state_variables_units = ['', '', '']
    parameters = ['a', 'b', 'c', 'd', 'f']
    parameters_units = ['', '', '']


class CModel(BaseModel):
    model: Union[SIR, SEIR, SEIRV]