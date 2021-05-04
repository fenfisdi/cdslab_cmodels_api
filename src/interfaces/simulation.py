from typing import Union
from uuid import UUID

from src.models.db.simulation import Simulation
from src.models.db.user import User


class SimulationInterface:

    @staticmethod
    def find_one_by_name(user: User, name: str) -> Simulation:
        filters = dict(
            user=user,
            name=name
        )
        return Simulation.objects(**filters).first()

    @staticmethod
    def find_one_by_uuid(user: User, uuid: Union[str, UUID]) -> Simulation:
        filters = dict(
            user=user,
            identifier=uuid
        )
        return Simulation.objects(**filters).first()

    @staticmethod
    def find_all(user: User):
        filters = dict(
            user=user
        )
        return Simulation.objects(**filters).all()
