import pytest
import requests

from web_app import constants
from .constants import URL


def test_auth():
    result = requests.post(f'{URL}/auth', data={'idul': 'gacou42'})

    assert result.status_code == 200
    assert 'token' in result.json()
    assert constants.TOKEN_PREFIX in result.json()['token']


@pytest.mark.parametrize('idul', ('gaco42', '12345', 'gacou'))
def test_auth_with_bad_idul(idul):
    result = requests.post(f'{URL}/auth', data={'idul': idul})

    assert result.status_code == 404
    assert 'error' in result.json()
    assert result.json()['error'] == f'No account "{idul}".'


def test_auth_without_idul():
    result = requests.post(f'{URL}/auth')

    assert result.status_code == 400
    assert 'error' in result.json()
    assert result.json()['error'] == f'IDUL not provided'
