import io

import pydicom
from pydicom.filebase import DicomBytesIO, DicomFileLike


def read_dicom_dataset(raw_data: bytes) -> pydicom.Dataset:
    buffer = DicomBytesIO(raw_data)

    return pydicom.dcmread(buffer)


def dicom_dataset_to_bytes(ds: pydicom.Dataset) -> io.BytesIO:
    buffer = io.BytesIO()
    memory_dataset = DicomFileLike(buffer)
    pydicom.dcmwrite(memory_dataset, ds)
    memory_dataset.seek(0)

    return buffer
