from typing import Union
from uuid import UUID

from src.models.db.simulation import Simulation
from src.models.db.user import User
from src.utils.date_time import DateTime


class SimulationInterface:
    """
        Class to query the user db
    """
    @staticmethod
    def find_one_by_name(user: User, name: str) -> Simulation:
        """
        find a simulation that matches the name and user
    
        :param name: Simulation name.
        :param user: Simulation user.
        """
        filters = dict(
            user=user,
            name=name,
            is_deleted=False,
        )
        return Simulation.objects(**filters).first()

    @staticmethod
    def find_one_by_uuid(user: User, uuid: Union[str, UUID]) -> Simulation:
        """
        find a simulation that matches the uuid and user

        :param user: Simulation user
        :param uuid: simulation uuid
        """
        filters = dict(
            user=user,
            identifier=uuid,
            is_deleted=False,
        )
        return Simulation.objects(**filters).first()

    @staticmethod
    def find_all(user: User):
        """
        find simulations matching user
        
        :param user: Simulation user
        """
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
