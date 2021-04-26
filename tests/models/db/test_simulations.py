import pytest
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pydantic import ValidationError

from src.models.db.simulations import (
    SimulationType,
    SimulationConfig,
)


sim_config = {
    'id': ObjectId(),
    'user_id': ObjectId(),
    'simulation_name': 'whatever',
    'cmodel_id': ObjectId('6083175ea91f5aacea234423'),
    'optimize_parameters': True,
    'dates_interval': (
        datetime.utcnow(),
        datetime.utcnow() + timedelta(days=10)
    ),
    'parameters_limits': {'a': (3, 4), 'b': (1, 2)},
    'state_variables_init_vals': {'S': 1, 'I': 2, 'R': 3},
    'state_variable_to_fit': 'S',
    'attached_time_series': None
}


def test_SimulationType():
    assert len(SimulationType) == 2
    assert SimulationType.optimize.value == 'Optimize parameters'
    assert SimulationType.fixed.value == 'Fixed parameters'


def test_SimulationConfig():
    SimulationConfig(
        **sim_config
    )


def test_SimulationConfig_forbiden_field():
    with pytest.raises(ValidationError):
        SimulationConfig(
            **{**sim_config, **{'bad_field_name': 'random value'}}
        )


def test_SimulationConfig_bad_time_limits():
    with pytest.raises(ValidationError):
        SimulationConfig(
            **{
                ** sim_config,
                ** {
                    'dates_interval':
                    (datetime.utcnow(), datetime.utcnow() - timedelta(days=10))
                }
            }
        )


def test_SimulationConfig_bad_parameter_name():
    with pytest.raises(ValidationError):
        SimulationConfig(
            **{
                **sim_config,
                **{
                    'parameters_limits': {'a': (3, 4), 'd': (1, 2)}
                }
            }
        )


def test_SimulationConfig_bad_cmodel_id():
    with pytest.raises(ValidationError):
        SimulationConfig(
            **{
                'id': ObjectId(),
                'user_id': ObjectId(),
                'simulation_name': 'whatever',
                'cmodel_id': ObjectId('6083175ea91f5aacea123456'),
                'optimize_parameters': True,
                'dates_interval': (
                    datetime.utcnow(),
                    datetime.utcnow() + timedelta(days=10)
                ),
                'parameters_limits': {'a': (3, 4), 'b': (1, 2)},
                'state_variables_init_vals': {'S': 1, 'I': 2, 'R': 3},
                'state_variable_to_fit': 'S',
                'attached_time_series': None
            }
        )


def test_SimulationConfig_bad_parameter_limits():
    with pytest.raises(ValidationError):
        SimulationConfig(
            **{
                **sim_config,
                **{'parameters_limits': {'a': (5, 1), 'b': (1, 2)}}
            }
        )
