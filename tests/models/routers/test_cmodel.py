from hypothesis import given, strategies as st

from src.models.routers.cmodel import (
    CompartmentalModelBase,
    CompartmentalModel,
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


def test_CompartmentalModel():
    for model in CompartmentalModel:
        assert isinstance(model.value, CompartmentalModelBase)


@given(st.builds(CModel))
def test_CModel(instance: CModel):
    assert isinstance(instance.model, CompartmentalModel)


@given(st.builds(AllCModels))
def test_AllCmodels(instance: AllCModels):
    for model in instance.models:
        assert isinstance(model, CompartmentalModelBase)
