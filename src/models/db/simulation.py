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

from src.models.general import DataSourceType, ParameterType, SimulationStatus
from .base import BaseDocument
from .model import Model
from .user import User


class Parameter(EmbeddedDocument):
    label = StringField()
    representation = StringField()
    type = EnumField(ParameterType)
    value = FloatField(null=True)
    min_value = FloatField(null=True)
    max_value = FloatField(null=True)


class VariableState(EmbeddedDocument):
    label = StringField()
    representation = StringField()
    value = FloatField()
    to_fit = BooleanField(default=False)


class Simulation(BaseDocument):
    name = StringField(required=True)
    model_name = StringField()
    identifier = UUIDField(unique=True, required=True)
    parameter_type = EnumField(ParameterType)
    interval_date = ListField()
    parameters_limits = EmbeddedDocumentListField(Parameter)
    state_variable_limits = EmbeddedDocumentListField(VariableState)
    status = EnumField(SimulationStatus, required=True)
    data_source = EnumField(DataSourceType, null=True)
    model = ReferenceField(Model, dbref=True)
    user = ReferenceField(User, dbref=True)
    is_deleted = BooleanField(default=False)
