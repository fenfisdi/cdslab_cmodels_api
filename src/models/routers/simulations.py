from typing import Tuple, Dict, Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator

from src.models.general_config import GeneralConfig, PydanticObjectId
from src.models.db.cmodels import CompartmentalModelEnum


class SimulationConfig(BaseModel):
    user_id: PydanticObjectId
    simulation_name: str = Field(..., max_length=50)
    """Custom name of simulation given by user"""
    cmodel_id: PydanticObjectId
    """Compartmental Model iD in mongodb"""
    optimize_parameters: bool
    """``True`` means optimize parameters, ``False`` means fixed parameters."""
    dates_interval: Tuple[datetime, datetime]
    """initial and final dates"""
    parameters_limits: Dict[str, Tuple[float, Optional[float]]]
    """{'<parameter_name>': (min_value, max_value)}"""
    state_variables_init_vals: Dict[str, float]
    """Must be given when ``optimize_parameters`` is true
    schema: ``{'<state_variable_name>': initial_value (float)}``
    """
    state_variable_to_fit: Optional[str]
    """Must be given when ``optimize_parameters`` is true"""

    @validator('cmodel_id', check_fields=False, pre=True)
    def cmodel_exists(cls, v):
        """Validates that cmodel exists in database"""
        for cmodel in CompartmentalModelEnum.values():
            if cmodel.id == v:
                return v
        raise ValueError('Compartmental model not found')

    @validator('dates_interval')
    def dates_start_end(cls, v: Tuple[datetime, datetime], **kwargs):
        """Validates that initial date is before final date"""
        if v[0] < v[1]:
            return v
        else:
            raise ValueError('Initial date must be before final date.')

    @validator('parameters_limits', check_fields=False)
    def appropiate_parameters_names(
        cls,
        v: Dict[str, Tuple[float, float]],
        values
    ):
        """Validates that given parameters correspond to parameters of
        chosen compartmental model.
        """
        for cmodel in CompartmentalModelEnum.values():
            if (
                'cmodel_id' in values.keys()
                and cmodel.id == values['cmodel_id']
                and set(cmodel.parameters) == set(v.keys())
            ):
                return v

        raise ValueError(
            'parameters_limits keys do not correspond with chosen '
            'compartmental model.'
        )

    @validator('parameters_limits', check_fields=False)
    def appropiate_parameters_limits(
        cls,
        v: Dict[str, Tuple[float, float]]
    ):
        """Validates that minimum limit is less than maximum limit"""
        for _, limits in v.items():
            if limits[0] >= limits[1] and not (limits[1] is None):
                raise ValueError(
                    'minimum value should be less than maximum value.'
                )

        return v

    @validator('state_variables_init_vals', check_fields=False)
    def appropiate_state_variables(cls, v: Dict[str, str], values, **kwargs):
        """Validates that given state variables correspond to state variables
        of chosen compartmental model.
        """
        for cmodel in CompartmentalModelEnum.values():
            if (
                'cmodel_id' in values.keys()
                and cmodel.id == values['cmodel_id']
                and set(cmodel.state_variables) == set(v.keys())
            ):
                return v

        raise ValueError(
            'Parameter names do not correspond with chosen '
            'compartmental model.'
        )

    @validator('state_variable_to_fit')
    def valid_state_variable(cls, v: Optional[str], values: dict):
        for cmodel in CompartmentalModelEnum.values():
            if (
                'cmodel_id' in values.keys()
                and cmodel.id == values['cmodel_id']
                and v in cmodel.state_variables
            ):
                return v
            raise ValueError(
                'Not a valid state variable for given'
                'compartmentalmodel'
            )

    class Config(GeneralConfig):
        ...
