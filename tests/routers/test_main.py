import requests
from dotenv import dotenv_values

server_settings = dotenv_values('.env')

def test_hello():
    request = requests.get(server_settings['DOMAIN'])
    assert request.json() == {'hello': 'world'}
