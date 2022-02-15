import pytest
import requests

from .constants import URL

TOKEN = 'e2a2f3d81a0de2ba37bb821c9e16c7960e21cf84'


def test_retrieve_data():
    result = requests.get(f'{URL}/data/dose', params={'token': TOKEN})

    assert result.status_code == 200
    with open('wep_app/data/rtdose.dcm', 'rb') as file:
        assert result.content == file.read()


def test_retrieve_data_with_bad_data_type():
    result = requests.get(f'{URL}/data/bad_data_type', params={'token': TOKEN})

    assert result.status_code == 400
    assert result.json() == {'error': 'Must provide data type ("structure" or "dose"). "bad_data_type" was provided'}


@pytest.mark.parametrize('token', ('gacou42', 'alsjdlkasjd', '123'))
def test_retrieve_data_with_bad_token(token):
    result = requests.get(f'{URL}/data/dose', params={'token': token})

    assert result.status_code == 401
    assert result.json() == {'error': 'Not authorized'}
