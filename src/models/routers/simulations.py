from typing import Tuple, Dict, Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator
from bson.objectid import ObjectId as BsonObjectId

from src.models.general_config import GeneralConfig, PydanticObjectId
from src.models.db.cmodels import CompartmentalModelEnum


DatesIntervalType = Tuple[datetime, datetime]
ParamsLimitsType = Dict[str, Tuple[float, float]]
StateVarsType = Dict[str, float]
StateVarFitType = Optional[str]


class SimulationConfig(BaseModel):
    user_id: PydanticObjectId
    simulation_name: str = Field(..., max_length=50)
    """Custom name of simulation given by user"""
    cmodel_id: PydanticObjectId
    """Compartmental Model iD in mongodb"""
    optimize_parameters: bool
    """``True`` means optimize parameters, ``False`` means fixed parameters."""
    dates_interval: DatesIntervalType
    """initial and final dates"""
    parameters_limits: ParamsLimitsType
    """{'<parameter_name>': (min_value, max_value)}. ``min_value == max_value``
    will be interpreted as a constant parameter.
    """
    state_variables_init_vals: StateVarsType
    """Must be given when ``optimize_parameters`` is true
    schema: ``{'<state_variable_name>': initial_value (float)}``
    """
    state_variable_to_fit: StateVarFitType
    """Must be given when ``optimize_parameters`` is true"""

    @validator('cmodel_id', check_fields=False, pre=True)
    def cmodel_exists(cls, v: BsonObjectId):
        """Validates that cmodel exists in database"""
        for cmodel in CompartmentalModelEnum.values():
            if cmodel.id == v:
                return v
        raise ValueError('Compartmental model not found')

    @validator('dates_interval')
    def dates_start_end(cls, v: DatesIntervalType, **kwargs):
        """Validates that initial date is before final date"""
        if v[0] < v[1]:
            return v
        else:
            raise ValueError('Initial date must be before final date.')

    @validator('parameters_limits', check_fields=False)
    def appropriate_parameters_names(cls, v: ParamsLimitsType, values):
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
    def appropriate_parameters_limits(cls, v: ParamsLimitsType):
        """Validates that minimum limit is less than maximum limit"""
        for _, limits in v.items():
            if limits[0] > limits[1]:
                raise ValueError(
                    'minimum value should be less than or equal to maximum '
                    'value.'
                )

        return v

    @validator('state_variables_init_vals', check_fields=False)
    def appropriate_state_vars_names(cls, v: StateVarsType, values, **kwargs):
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
            'State variables\' names do not correspond with chosen '
            'compartmental model.'
        )

    @validator('state_variable_to_fit')
    def valid_state_variable_fit(cls, v: StateVarFitType, values: dict):
        for cmodel in CompartmentalModelEnum.values():
            if (
                'cmodel_id' in values.keys()
                and cmodel.id == values['cmodel_id']
                and v in cmodel.state_variables
            ):
                return v
            raise ValueError(
                'Not a valid state variable for given compartmental model.'
            )

    class Config(GeneralConfig):
        ...
