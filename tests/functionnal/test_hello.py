import requests

from .constants import URL


def test_hello():
    result = requests.get(f'{URL}/')

    assert result.json() == {'message': "Bonjour et bienvenue au workshop sur le Web!"}
