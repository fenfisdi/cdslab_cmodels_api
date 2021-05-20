from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from pydantic import BaseModel, Field, root_validator

from src.models.general import DataSourceType, ParameterType, SimulationStatus


class Parameter(BaseModel):
    label: str = Field(...)
    representation: str = Field(...)
    type: ParameterType = Field(ParameterType.FIXED)
    value: float = Field(None)
    min_value: float = Field(None)
    max_value: float = Field(None)

    @root_validator
    def validate_type(cls, values):
        parameter_type = values.get('type')

        # Verify value field if type is fixed
        if parameter_type == ParameterType.FIXED:
            value = values.get('value')
            assert isinstance(value, float), 'value must be set'
            values['min_value'] = None
            values['max_value'] = None

        # Verify min_value and max_value if type is optimized
        elif parameter_type == ParameterType.OPTIMIZED:
            min_value = values.get('min_value')
            max_value = values.get('max_value')
            is_values_set = (
                    isinstance(min_value, float) or isinstance(max_value, float)
            )
            assert is_values_set, 'min_value and max_value must be set'
            if min_value >= max_value:
                raise ValueError('max_value must be greater than min_value')

            values['value'] = None

        return values


class StateVariable(BaseModel):
    label: str = Field(...)
    representation: str = Field(...)
    value: float = Field(...)
    to_fit: bool = Field(False)


class UpdateSimulation(BaseModel):
    name: str = Field(None)
    status: SimulationStatus = Field(SimulationStatus.INCOMPLETE)
    parameter_type: ParameterType = Field(None)
    interval_date: Tuple[datetime, datetime] = Field(None)
    parameters_limits: List[Parameter] = Field(None, min_items=0)
    state_variable_limits: List[StateVariable] = Field(None, min_items=0)
    data_source: DataSourceType = Field(None)


class NewSimulation(UpdateSimulation):
    name: str = Field(...)
    model_id: UUID = Field(...)
