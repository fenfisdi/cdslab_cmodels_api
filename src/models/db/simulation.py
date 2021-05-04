from mongoengine import (
    ReferenceField,
    StringField,
    BooleanField,
    ListField,
    DictField,
    UUIDField
)

from .base import BaseDocument
from .model import Model
from .user import User


class Simulation(BaseDocument):
    name = StringField(unique_with='user')
    identifier = UUIDField(unique=True)
    optimize_parameters = BooleanField()
    interval_date = ListField()
    parameters_limits = DictField()
    state_variables_init_vals = DictField()
    state_variable_to_fit = DictField()
    model = ReferenceField(Model)
    user = ReferenceField(User)
