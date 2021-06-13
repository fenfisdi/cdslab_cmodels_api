import re
from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, root_validator, validator

from src.models.general import DataSourceType, ParameterType, SimulationStatus

FORMAT_DATE = r'^\d{4}-\d{2}-\d{2}$'


class Parameter(BaseModel):
    label: str = Field(...)
    representation: str = Field(...)
    type: ParameterType = Field(ParameterType.FIXED)
    value: float = Field(None)
    unit: str = Field("")
    min_value: float = Field(None)
    max_value: float = Field(None)

    @root_validator
    def validate_type(cls, values):
        parameter_type = values.get('type')

        # Verify value field if type is fixed
        if parameter_type == ParameterType.FIXED:
            value = values.get('value')
            assert isinstance(value, float), 'value must be set'

        # Verify min_value and max_value if type is optimized
        elif parameter_type == ParameterType.OPTIMIZED:
            min_value = values.get('min_value')
            max_value = values.get('max_value')
            is_values_set = (
                    isinstance(min_value, float) or isinstance(max_value, float)
            )
            assert is_values_set, 'min_value and max_value must be set'
            if min_value > max_value:
                raise ValueError('max_value must be greater than min_value')

        return values


class StateVariable(BaseModel):
    label: str = Field(...)
    representation: str = Field(...)
    value: float = Field(...)
    unit: str = Field("")
    to_fit: bool = Field(False)


class Interval(BaseModel):
    start: datetime = Field(...)
    end: datetime = Field(...)

    @root_validator
    def validate_dates(cls, values):
        if values.get('start') > values.get('end'):
            raise ValueError('end datetime must be great than start time')
        return values

    @validator('start', 'end', pre=True)
    def validate_date_format(cls, value):
        if re.search(FORMAT_DATE, value):
            return value + 'T00:00'
        return value


class UpdateSimulation(BaseModel):
    name: str = Field(None)
    status: SimulationStatus = Field(SimulationStatus.INCOMPLETE)
    parameter_type: ParameterType = Field(ParameterType.FIXED)
    interval_date: Interval = Field(None)
    parameters_limits: List[Parameter] = Field(None, min_items=0)
    state_variable_limits: List[StateVariable] = Field(None, min_items=0)
    data_source: DataSourceType = Field(None)


class NewSimulation(UpdateSimulation):
    name: str = Field(...)
    model_id: UUID = Field(...)
