from os import environ
from typing import Any, Tuple, Union
from uuid import UUID

from src.utils.response import UJSONResponse
from src.utils.response import to_response
from .service import API, APIService


class FileAPI:
    api_url = environ.get('FILE_API')
    request = APIService(API(api_url))

    @classmethod
    def create_folder(cls, simulation_uuid: UUID, email: str):
        data = {
            'email': email,
            'simulation_uuid': str(simulation_uuid),
        }
        response = cls.request.post(f'/root/folder', json=data)
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def upload_file(
        cls,
        simulation_uuid: str,
        data: Any = None
    ) -> Tuple[Union[dict, UJSONResponse], bool]:

        response = cls.request.post(
            f'/simulation/{simulation_uuid}/file',
            data=data
        )
        if not response.ok:
            return to_response(response), True
        return response.json(), False
