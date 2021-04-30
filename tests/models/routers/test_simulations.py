import pytest
from datetime import datetime, timedelta
from unittest import TestCase
from copy import deepcopy

from bson.objectid import ObjectId
from pydantic import ValidationError

from src.models.routers.simulations import (
    SimulationConfig,
)


sim_config = {
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
}


class SimulationConfigTestCase(TestCase):

    def setUp(self) -> None:
        self.sim_config = deepcopy(sim_config)

    def tearDown(self) -> None:
        del self.sim_config

    def assert_raises_validation_error(self, sim_config):
        with pytest.raises(ValidationError):
            SimulationConfig(**sim_config)

    def test_ok(self):
        SimulationConfig(**self.sim_config)

    def test_forbiden_field(self):
        self.sim_config['bad_field_name'] = 'not a valid field name'
        self.assert_raises_validation_error(self.sim_config)

    def test_bad_cmodel_id(self):
        self.sim_config['cmodel_id'] = ObjectId('6083175ea91f5aacea123456')
        self.assert_raises_validation_error(self.sim_config)

    def test_bad_time_limits(self):
        self.sim_config['dates_interval'] = (
            datetime.utcnow(),
            datetime.utcnow() - timedelta(days=10)
        )
        self.assert_raises_validation_error(self.sim_config)

    def test_bad_parameter_name(self):
        self.sim_config['parameters_limits'] = {'a': (3, 4), 'd': (1, 2)}
        self.assert_raises_validation_error(self.sim_config)

    def test_bad_parameter_limits(self):
        self.sim_config['parameters_limits'] = {'a': (5, 1), 'b': (1, 2)}
        self.assert_raises_validation_error(self.sim_config)

    def test_bad_state_variable_name(self):
        self.sim_config['state_variables_init_vals'] = {'Z': 1, 'I': 2, 'R': 3}
        self.assert_raises_validation_error(self.sim_config)

    def test_bad_state_variable_fit(self):
        self.sim_config['state_variable_to_fit'] = 'Z'
        self.assert_raises_validation_error(self.sim_config)
