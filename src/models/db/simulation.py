from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField, EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    EnumField,
    FloatField,
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
    unit = StringField(null=False)
    min_value = FloatField(null=True)
    max_value = FloatField(null=True)


class VariableState(EmbeddedDocument):
    label = StringField()
    representation = StringField()
    value = FloatField()
    unit = StringField(null=False)
    to_fit = BooleanField(default=False)


class Interval(EmbeddedDocument):
    start = DateTimeField()
    end = DateTimeField()


class Simulation(BaseDocument):
    name = StringField(required=True)
    model_name = StringField()
    identifier = UUIDField(binary=False, unique=True, required=True)
    parameter_type = EnumField(ParameterType, null=False)
    interval_date = EmbeddedDocumentField(Interval, null=True)
    parameters_limits = EmbeddedDocumentListField(Parameter)
    state_variable_limits = EmbeddedDocumentListField(VariableState)
    status = EnumField(SimulationStatus, required=True)
    execution_time = DictField(null=True)
    data_source = EnumField(DataSourceType, null=True)
    model = ReferenceField(Model, dbref=True)
    user = ReferenceField(User, dbref=True)
    is_deleted = BooleanField(default=False)
