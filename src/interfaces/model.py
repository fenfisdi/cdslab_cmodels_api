from typing import Union
from uuid import UUID

from src.models.db.model import Model


class ModelInterface:
    """
        Class to query the user db
    """
    @staticmethod
    def find_one_by_name(model_name: str) -> Model:
        """
        find a model that matches the model name
        
        :param model_name: Model name.
        """
        filters = dict(
            name=model_name
        )
        return Model.objects(**filters).first()

    @staticmethod
    def find_one_by_uuid(uuid: Union[str, UUID]) -> Model:
        """
        find a model that matches the uuid
        :param uuid: Model uuid.
        """
        filters = dict(
            identifier=uuid,
        )
        return Model.objects(**filters).first()

    @staticmethod
    def find_all():
        """
        find all models
        """
        return Model.objects().all()
