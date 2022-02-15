import pytest
import requests

from .constants import URL

TOKEN = 'e2a2f3d81a0de2ba37bb821c9e16c7960e21cf84'


def test_retrieve_data():
    result = requests.get(f'{URL}/data', data={'token': TOKEN})

    assert result.status_code == 200
    assert result.json() == False


@pytest.mark.parametrize('token',('gacou42', '', '123qlakdjalksdj'))
def test_retrieve_data_with_bad_token(token):
    result = requests.get(f'{URL}/data', data={'token': TOKEN})

    assert result.status_code == 401
    assert result.json() == False
