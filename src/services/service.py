from dataclasses import dataclass
from typing import Any

from requests import Request, Session
from requests.models import Response


@dataclass
class API:
    '''
        Class that contains API URL
    '''
    url: str


class APIService:
    '''
        Class for configuring http requests (get and publish)   
    '''

    def __init__(self, api: API):
        '''
            Class constructor
        Pamaraters:
            api (API): API URL
        Return:
            None
        '''
        self.api = api
        self.session = Session()

    def __url(self, endpoint: str) -> str:
        '''
            Join URL to endpoint
        Parameters:
            endpoint (str): API endpoint
        Returns:
            str: URL concatenated with endpoint
        '''
        return "".join([self.api.url, endpoint])

    def post(
            self,
            endpoint: str,
            json: dict = None,
            data: Any = None,
            parameters: dict = None,
            files: Any = None
        ) -> Response:
        '''
            Execute a post request
        Parameters:
            endpoint (str): API endpoint
            json (dict): body of request
            data (any): data for request
            parameters (dict): parameters for request
            files (any): files for request
        Return:
            Response: API response
        '''
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
        '''
            Execute a get request
        Parameters:
            endpoint (str): API endpoint
            parameters (str): parameters for request
        Return:
            Response: API response
        '''
        request = Request(
            url=self.__url(endpoint),
            method='GET',
            params=parameters
        ).prepare()
        return self.session.send(request)
