from mongoengine import (
    ReferenceField,
    StringField,
    BooleanField,
    ListField,
    DictField,
    UUIDField,
    EnumField
)

from src.models.general import SimulationStatus
from .base import BaseDocument
from .model import Model
from .user import User


class Simulation(BaseDocument):
    name = StringField()
    identifier = UUIDField(unique=True, required=True)
    optimize_parameters = BooleanField()
    interval_date = ListField()
    parameters_limits = DictField()
    state_variables_init_vals = DictField()
    state_variable_to_fit = DictField()
    status = EnumField(SimulationStatus, required=True)
    model = ReferenceField(Model, dbref=True)
    user = ReferenceField(User, dbref=True)
    is_deleted = BooleanField(default=False)
