from dataclasses import dataclass
from typing import Any

from requests import Request, Session
from requests.models import Response


@dataclass
class API:
    """
        Class that contains API URL
    """
    url: str


class APIService:
    """
        Class for configuring http requests (get and publish)   
    """

    def __init__(self, api: API):
        """
        Class constructor
        :param api: API URL
        """
        self.api = api
        self.session = Session()

    def __url(self, endpoint: str) -> str:
        """
        Join URL to endpoint
        :param endpoint: API endpoint
        """
        return "".join([self.api.url, endpoint])

    def post(
            self,
            endpoint: str,
            json: dict = None,
            data: Any = None,
            parameters: dict = None,
            files: Any = None
        ) -> Response:
        """
        Execute a post request
        :param endpoint: API endpoint
        :param json: body of request
        :param data: data for request
        :param parameters: parameters for request
        :param files: files for request
        """
        request = Request(
            url=self.__url(endpoint),
            method='POST',
            params=parameters,
            json=json,
            data=data,
            files=files
        ).prepare()
        return self.session.send(request)

    def get(self, endpoint: str, parameters: dict = None) -> Response:
        """
        Execute a get request
        :param endpoint: API endpoint
        :param parameters: parameters for request
        """
        request = Request(
            url=self.__url(endpoint),
            method='GET',
            params=parameters
        ).prepare()
        return self.session.send(request)
