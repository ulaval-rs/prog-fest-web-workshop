import pytest
import requests

from .constants import URL

TOKEN = 'e2a2f3d81a0de2ba37bb821c9e16c7960e21cf84'


def test_retrieve_available_data():
    result = requests.get(f'{URL}/data', params={'token': TOKEN})

    assert result.status_code == 200
    assert result.json() == ['sphere', 'cylinder', 'cone', 'dose']


def test_retrieve_structure():
    result = requests.get(f'{URL}/data/sphere', params={'token': TOKEN})

    assert result.status_code == 200
    with open('web_app/data/rtstruct-sphere.dcm', 'rb') as file:
        assert result.content == file.read()


def test_retrieve_dose():
    result = requests.get(f'{URL}/data/dose', params={'token': TOKEN})

    assert result.status_code == 200
    with open('web_app/data/rtdose.dcm', 'rb') as file:
        assert result.content == file.read()


def test_retrieve_data_with_bad_data_type():
    result = requests.get(f'{URL}/data/bad_data_type', params={'token': TOKEN})

    assert result.status_code == 404
    assert result.json() == {'error': f'Data type "bad_data_type" not found. Accepted data type are ("structure" or "dose").'}


@pytest.mark.parametrize('token', ('gacou42', 'alsjdlkasjd', '123'))
def test_retrieve_data_with_bad_token(token):
    result = requests.get(f'{URL}/data/dose', params={'token': token})

    assert result.status_code == 401
    assert result.json() == {'error': 'Not authorized'}


def test_retrieve_data_without_token():
    result = requests.get(f'{URL}/data/dose')

    assert result.status_code == 400
    assert result.json() == {'error': 'Token not provided'}

