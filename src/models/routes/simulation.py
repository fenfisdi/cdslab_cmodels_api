from datetime import datetime
from typing import Tuple, List
from uuid import UUID

from pydantic import BaseModel, Field, root_validator

from src.models.general import ParameterType, SimulationStatus


class Parameter(BaseModel):
    label: str = Field(...)
    type: ParameterType = Field(...)
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

        return values


class UpdateSimulation(BaseModel):
    name: str = Field(None)
    status: SimulationStatus = Field(SimulationStatus.INCOMPLETE)
    optimize_parameters: bool = Field(None)
    interval_date: Tuple[datetime, datetime] = Field(None)
    parameters_limits: List[Parameter] = Field(None)
    state_variables_init_vals: dict = Field(None)
    state_variable_to_fit: dict = Field(None)


class NewSimulation(UpdateSimulation):
    model_id: UUID = Field(...)
