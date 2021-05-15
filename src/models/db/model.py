from mongoengine import (
    StringField,
    UUIDField,
    FloatField,
    EmbeddedDocument,
    EmbeddedDocumentListField

)

from .base import BaseDocument


class Parameter(EmbeddedDocument):
    label = StringField()
    representation = StringField()
    unit = StringField()
    min_value = FloatField()
    max_value = FloatField()


class StateVariable(EmbeddedDocument):
    label = StringField()
    name = StringField()
    unit = StringField()


class Model(BaseDocument):
    name = StringField(unique=True)
    identifier = UUIDField(unique=True, required=True)
    state_variables = EmbeddedDocumentListField(StateVariable)
    parameters = EmbeddedDocumentListField(Parameter)
