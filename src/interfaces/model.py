from typing import Union
from uuid import UUID

from src.models.db.model import Model


class ModelInterface:

    @staticmethod
    def find_one_by_name(model_name: str) -> Model:
        filters = dict(
            name=model_name
        )
        return Model.objects(**filters).first()

    @staticmethod
    def find_one_by_uuid(uuid: Union[str, UUID]) -> Model:
        filters = dict(
            identifier=uuid,
        )
        return Model.objects(**filters).first()

    @staticmethod
    def find_all():
        return Model.objects()
