import pytest
from fastapi.testclient import TestClient
from requests.models import Response

from src.api import app


client = TestClient(app)

root_route = '/'


def test_hello():
    response = client.get(root_route)
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}


@pytest.mark.parametrize(
    'response',
    [
        client.post(root_route),
        client.put(root_route),
        client.delete(root_route),
        client.patch(root_route)
    ]
)
def test_hello_bad_request_method(
    response: Response
):
    assert response.status_code == 405
