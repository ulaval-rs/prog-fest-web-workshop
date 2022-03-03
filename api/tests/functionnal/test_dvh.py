import requests
import pytest

from tests.functionnal.constants import URL


@pytest.fixture
def dose():
    with open('./web_app/data/rtdose.dcm', 'rb') as file:
        return file.read()


@pytest.fixture
def struct():
    with open('./web_app/data/rtstruct-sphere.dcm', 'rb') as file:
        return file.read()


def test_dvh_calculation(struct, dose):
    result = requests.post(f'{URL}/dvh', files={'file_dose': dose, 'file_struct': struct})

    assert result.status_code == 200
    assert isinstance(result.json(), list)
    assert result.json()[1]['name'] == 'Sphere_02_0'
    assert result.json()[1]['type'] == 'cumulative'
    assert result.json()[1]['volume'] == 7.185399999999974
    assert result.json()[1]['volume_units'] == 'cm3'
    assert result.json()[1]['dose_units'] == 'Gy'


@pytest.mark.parametrize('rtstruct, rtdose', [
    (open('./web_app/data/rtdose.dcm', 'rb').read(), open('./web_app/data/rtdose.dcm', 'rb').read()),
    (open('./web_app/data/rtstruct-sphere.dcm', 'rb').read(), open('./web_app/data/rtstruct-sphere.dcm', 'rb').read()),
])
def test_dvh_calculation_with_bad_data(rtstruct, rtdose):
    result = requests.post(f'{URL}/dvh', files={'file_dose': rtdose, 'file_struct': rtstruct})

    assert result.status_code == 400


def test_dvh_calculation_with_missing_data(struct):
    result = requests.post(f'{URL}/dvh', files={'file_struct': struct})

    assert result.status_code == 400
    assert result.json() == {'error': '"file_dose" or "file_struct" not provided'}

