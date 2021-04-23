import pytest
from hypothesis import given, strategies as st

from src.models.db.cmodels import (
    CompartmentalModelBase,
    CompartmentalModelEnum,
    CModel,
    AllCModels,
)


@given(st.builds(CompartmentalModelBase))
def test_CompartmentalModelBase_properties(instance: CompartmentalModelBase):
    assert isinstance(instance.name, str)
    assert isinstance(instance.state_variables, list)
    assert isinstance(instance.state_variables_units, dict)
    assert isinstance(instance.parameters, list)
    assert isinstance(instance.parameters_units, dict)


@pytest.mark.parametrize('model', [model for model in CompartmentalModelEnum])
def test_CompartmentalModel(model: CompartmentalModelEnum):
    assert isinstance(model.value, CompartmentalModelBase)


@given(st.builds(CModel))
def test_CModel(instance: CModel):
    assert isinstance(instance.model, CompartmentalModelEnum)


@given(st.builds(AllCModels))
def test_AllCmodels(instance: AllCModels):
    for model in instance.models:
        assert isinstance(model, CompartmentalModelBase)


print(CompartmentalModelEnum.values()[0])
