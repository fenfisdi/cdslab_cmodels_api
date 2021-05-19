from mongoengine import (EmbeddedDocument, EmbeddedDocumentListField,
                         FloatField, StringField, UUIDField)

from .base import BaseDocument


class Parameter(EmbeddedDocument):
    label = StringField()
    representation = StringField()
    unit = StringField()
    min_value = FloatField()
    max_value = FloatField()


class StateVariable(EmbeddedDocument):
    label = StringField()
    representation = StringField()
    unit = StringField()


class Model(BaseDocument):
    name = StringField(unique=True)
    identifier = UUIDField(unique=True, required=True)
    state_variables = EmbeddedDocumentListField(StateVariable)
    parameters = EmbeddedDocumentListField(Parameter)
