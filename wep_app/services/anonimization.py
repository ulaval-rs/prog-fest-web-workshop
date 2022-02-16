import pydicom


class AnonymizationService:

    def anonymize(self, ds: pydicom.Dataset) -> pydicom.Dataset:
        ds.PatientName = '^'

        return ds
