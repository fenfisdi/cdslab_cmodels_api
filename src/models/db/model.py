from mongoengine import (
    BooleanField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    FloatField,
    StringField,
    UUIDField
)

from .base import BaseDocument


class Parameter(EmbeddedDocument):
    label = StringField()
    representation = StringField()
    description = StringField()
    unit = StringField()
    min_value = FloatField()
    max_value = FloatField()


class StateVariable(EmbeddedDocument):
    label = StringField()
    representation = StringField()
    description = StringField()
    unit = StringField()
    can_fit = BooleanField(default=True)


class Model(BaseDocument):
    name = StringField(unique=True)
    identifier = UUIDField(binary=False, unique=True, required=True)
    state_variables = EmbeddedDocumentListField(StateVariable)
    parameters = EmbeddedDocumentListField(Parameter)
