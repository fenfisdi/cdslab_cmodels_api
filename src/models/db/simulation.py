from mongoengine import (
    BooleanField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EnumField,
    FloatField,
    ListField,
    ReferenceField,
    StringField,
    UUIDField
)

from src.models.general import ParameterType, SimulationStatus
from .base import BaseDocument
from .model import Model
from .user import User


class Parameter(EmbeddedDocument):
    label = StringField()
    type = EnumField(ParameterType)
    value = FloatField()
    min_value = FloatField()
    max_value = FloatField()


class VariableState(EmbeddedDocument):
    label = StringField()
    value = FloatField()
    to_fit = BooleanField(default=False)


class Simulation(BaseDocument):
    name = StringField()
    identifier = UUIDField(unique=True, required=True)
    optimize_parameters = BooleanField()
    interval_date = ListField()
    parameters_limits = EmbeddedDocumentListField(Parameter)
    state_variable_limits = EmbeddedDocumentListField(VariableState)
    status = EnumField(SimulationStatus, required=True)
    model = ReferenceField(Model, dbref=True)
    user = ReferenceField(User, dbref=True)
    is_deleted = BooleanField(default=False)
