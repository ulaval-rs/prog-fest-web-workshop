import pydicom
import pytest
import requests
from pydicom.filebase import DicomBytesIO

from tests.functionnal.constants import URL


@pytest.fixture
def dicom_file():
    with open('./wep_app/data/rtdose.dcm', 'rb') as file:
        return file.read()


@pytest.fixture
def bad_file():
    with open('./app.py', 'rb') as file:
        return file.read()


def test_anonymization(dicom_file):
    result = requests.post(f'{URL}/anonymize', files={'file': dicom_file})

    assert result.status_code == 200
    ds = pydicom.dcmread(DicomBytesIO(result.content))
    assert ds.PatientName == '^'


def test_anonymization_with_bad_file(bad_file):
    result = requests.post(f'{URL}/anonymize', files={'file': bad_file})

    assert result.status_code == 400
    assert result.json() == {'error': 'Invalid DICOM file'}


def test_anonymization_without_file():
    result = requests.post(f'{URL}/anonymize')

    assert result.status_code == 400
    assert result.json() == {'error': 'File not provided'}
