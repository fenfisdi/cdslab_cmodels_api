from uuid import uuid1

from mongoengine import StringField, ListField, UUIDField

from .base import BaseDocument


class Model(BaseDocument):
    name = StringField(unique=True)
    uuid = UUIDField(default=uuid1(), unique=True)
    state_variables = ListField()
    parameters = ListField()
