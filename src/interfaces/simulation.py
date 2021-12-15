from typing import Union
from uuid import UUID

from src.models.db.simulation import Simulation
from src.models.db.user import User
from src.utils.date_time import DateTime


class SimulationInterface:

    @staticmethod
    def find_one_by_name(user: User, name: str) -> Simulation:
        filters = dict(
            user=user,
            name=name,
            is_deleted=False,
        )
        return Simulation.objects(**filters).first()

    @staticmethod
    def find_one_by_uuid(user: User, uuid: Union[str, UUID]) -> Simulation:
        filters = dict(
            user=user,
            identifier=uuid,
            is_deleted=False,
        )
        return Simulation.objects(**filters).first()

    @staticmethod
    def find_all(user: User):
        filters = dict(
            user=user,
            is_deleted=False,
        )
        return Simulation.objects(**filters).all()


class RootSimulationInterface:

    @staticmethod
    def find_all_expired(days_to_expire: int):
        filters = dict(
            updated_at__lt=DateTime.expiration_date(days=days_to_expire)
        )
        return Simulation.objects(**filters).all()
