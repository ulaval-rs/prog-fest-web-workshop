import pytest
import requests

from web_app import constants
from .constants import URL


def test_create_account():
    result = requests.post(f'{URL}/account', data={'idul': 'gacou42'})

    assert result.status_code == 201
    assert result.json() == {'message': 'created'}


@pytest.mark.parametrize('idul', ('gaco42', '12345', 'gacou'))
def test_create_account_with_bad_idul(idul):
    result = requests.post(f'{URL}/account', data={'idul': idul})

    assert result.status_code == 400
    assert 'error' in result.json()
    assert result.json()['error'] == f'Bad IDUL: "{idul}"'


def test_create_account_without_idul():
    result = requests.post(f'{URL}/account')

    assert result.status_code == 400
    assert 'error' in result.json()
    assert result.json()['error'] == f'IDUL not provided'
