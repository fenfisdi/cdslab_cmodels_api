from mongoengine import StringField, ListField, UUIDField

from .base import BaseDocument


class Model(BaseDocument):
    name = StringField(unique=True)
    identifier = UUIDField(unique=True, required=True)
    state_variables = ListField()
    parameters = ListField()
