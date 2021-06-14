from mongoengine import (
    StringField
)

from .base import BaseDocument


class INSVariable(BaseDocument):
    label = StringField(unique=True)
    representation = StringField(unique=True)
    description = StringField(default="")
    unit = StringField(default="")
