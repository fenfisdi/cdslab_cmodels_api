from mongoengine import (
    ReferenceField,
    StringField,
    BooleanField,
    ListField,
    DictField
)

from .base import BaseDocument
from .model import Model
from .user import User


class Simulation(BaseDocument):
    model = ReferenceField(Model)
    user = ReferenceField(User)
    name = StringField(unique_with='user')
    optimize_parameters = BooleanField()
    dates_interval = ListField()
    parameters_limits = DictField()
    state_variables_init_vals = DictField()
    state_variable_to_fit = DictField()
