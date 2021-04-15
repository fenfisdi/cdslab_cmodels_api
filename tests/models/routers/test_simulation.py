from datetime import datetime

from hypothesis import given, strategies as st

from src.models.routers.simulation import (
    SimulationType,
    SimulationConfig,
    PydanticObjectId
)


def test_SimulationType():
    assert len(SimulationType) == 2
    assert SimulationType.optimize.value == 'Optimize parameters'
    assert SimulationType.fixed.value == 'Fixed parameters'


@given(st.builds(SimulationConfig))
def test_SimulationConfig(instance: SimulationConfig):
    assert isinstance(instance.user_id, PydanticObjectId)
    assert isinstance(instance.model_id, str)
    assert isinstance(instance.name, str)
    assert isinstance(instance.creation_date, datetime)
    assert isinstance(instance.simulation_type, SimulationType)
