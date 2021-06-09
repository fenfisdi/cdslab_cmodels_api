from os import environ
from typing import Union, Tuple

from src.utils.response import UJSONResponse
from src.utils.response import to_response
from .service import API, APIService


class UserAPI:
    """
        Handles API requests to FILE API
    """
    api_url = environ.get('USER_API')
    request = APIService(API(api_url))

    @classmethod
    def find_user(
        cls,
        email: str,
        is_valid: bool = True,
        is_enabled: bool = True
        ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Search for a user in USER API
        
        :param email: User email
        :param is_valid: User valid in BD
        :param is_enabled: User enabled in BD
        """
        parameters = {
            'is_valid': is_valid,
            'is_enabled': is_enabled,
        }
        response = cls.request.get(f'/user/{email}', parameters=parameters)
        if not response.ok:
            return to_response(response), True
        return response.json(), False
