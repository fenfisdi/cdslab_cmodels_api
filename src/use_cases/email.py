from src.models.db import Simulation, User
from src.services import ManagementAPI


class SendEmailUseCase:

    @classmethod
    def simulation_email(
        cls,
        simulation: Simulation,
        user: User,
        error: bool = False
    ):
        message = f'Your Simulation \'{simulation.name}\' ' \
                  f'\'{simulation.identifier}\' has been finished '
        message += "with errors" if error else "without errors"
        data = {
            'email': user.email,
            'subject': 'Simulation Executed',
            'message': message,
        }
        ManagementAPI.send_email(data)
