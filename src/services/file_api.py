from os import environ
from typing import Any, Tuple, Union
from uuid import UUID

from requests import Response

from src.utils.response import UJSONResponse
from src.utils.response import to_response
from .service import API, APIService
from ..models.routes import TypeFile


class FileAPI:
    '''
        Handles API requests to FILE API
    '''
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
        simulation_uuid: UUID,
        files: Any = None,
        file_type: TypeFile = TypeFile.DOWNLOAD
      ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """

        :param simulation_uuid:
        :param files:
        :param file_type:
        """

        parameters = {
            'file_type': file_type.value,
        }
        response = cls.request.post(
            f'/root/simulation/{str(simulation_uuid)}/file',
            parameters=parameters,
            files=files
        )
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def list_simulation_files(cls, simulation_uuid: UUID):
        """

        :param simulation_uuid:
        """

        response = cls.request.get(
            f'/root/simulation/{str(simulation_uuid)}/file'
        )
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_file(
        cls,
        simulation_uuid: UUID,
        file_uuid: UUID
      ) -> Tuple[Union[Response, UJSONResponse], bool]:

        response = cls.request.get(
            f'/root/simulation/{str(simulation_uuid)}/file/{str(file_uuid)}'
        )
        if not response.ok:
            return to_response(response), True
        return response, False


