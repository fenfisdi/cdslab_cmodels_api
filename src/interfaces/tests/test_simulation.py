from uuid import uuid1
from unittest import TestCase
from datetime import datetime

from mongoengine import connect, disconnect

from src.models.db.user import User
from src.models.db.model import (
    Model, 
    StateVariable,
    Parameter as ModelParam
)
from src.models.db.simulation import (
    Simulation,
    Interval,
    Parameter,
    VariableState   
)
from src.models.general import (
    DataSourceType, 
    ParameterType,
    SimulationStatus
)
from src.utils.encoder import BsonObject
from src.interfaces.simulation import SimulationInterface


class SimulationInterfaceTestCase(TestCase):
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.email = "test1@test.com"
        self.simulation_name = "TestSimulation"
        self.simulation_id = uuid1()
        self.model_id = uuid1()
        self.model_name = "test"
        
        self.user = User(
            name="testName",
            email=self.email
        )
        self.user.save()

        self.parameter = [ModelParam(
            label="test",
            representation="unittest",
            unit="unit",
            min_value=0.0,
            max_value=5.0
        )]
        
        self.state = [StateVariable(
            label="test",
            representation="unit",
            unit="unittest",
            can_fit=True
        )]

        self.model = Model(
            name=self.model_name,
            identifier=self.model_id,
            state_variables=self.state,
            parameters=self.parameter
        )
        self.model.save()

        Simulation(
            name=self.simulation_name,
            model_name=self.model_name,
            identifier=self.simulation_id,
            parameter_type=ParameterType.FIXED,
            interval_date=Interval(
                start=datetime.now(), 
                end=datetime.now()
            ),
            parameters_limits=[Parameter(
                label="test",
                representation="unittest",
                type=ParameterType.FIXED,
                value=4.0,
                min_value=0,
                max_value=5.0
            )],
            state_variable_limits=[VariableState(
                label="test",
                representation="unit",
                value=0.5,
                to_fit=True
            )],
            status=SimulationStatus.DONE,
            execution_time=None,
            data_source=DataSourceType.UPLOAD,
            model=self.model,
            user=self.user,
            is_deleted=False
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_by_name(self):
        simulation = SimulationInterface.find_one_by_name(
            user=self.user,
            name=self.simulation_name
        )

        self.assertIsNotNone(simulation)
        self.assertIsInstance(simulation, Simulation)
    
    def test_find_one_by_name_not_found(self):
        simulation = SimulationInterface.find_one_by_name(
            user=self.user,
            name=""
        )

        self.assertIsNone(simulation)

    def test_find_one_by_uuid(self):
        simulation = SimulationInterface.find_one_by_uuid(
            user=self.user,
            uuid=self.simulation_id
        )

        self.assertIsNotNone(simulation)
        self.assertIsInstance(simulation, Simulation)
        self.assertEqual(simulation.name, self.simulation_name)
    
    def test_find_one_by_uuid_not_found(self):
        simulation = SimulationInterface.find_one_by_uuid(
            user=self.user,
            uuid=uuid1()
        )

        self.assertIsNone(simulation)
    
    def test_find_all(self):
        simulation = SimulationInterface.find_all(
            user=self.user
        )

        simulations = BsonObject.dict(simulation)

        self.assertIsNotNone(simulation)
        self.assertTrue(len(simulations) > 0)
