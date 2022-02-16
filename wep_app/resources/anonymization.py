import io

import pydicom
from flask import request, send_file
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from pydicom.errors import InvalidDicomError
from pydicom.filebase import DicomBytesIO, DicomFileLike

from wep_app import services


class AnonymizationResource(Resource):

    def __init__(self, parser: RequestParser, anonymization_service: services.AnonymizationService):
        self.parser = parser
        self.anonymization_service = anonymization_service

    def post(self):
        """
        Anonymize
        ---
        tags:
            - Anonimisation
        parameters:
        - in: file
          name: Fichier DICOM
          required: true
          type: application/dicom
        responses:
            200:
                description: Anonymisé avec succès
                content:
                    application/dicom
            400:
                description: Fichier DICOM fourni invalide
        """
        if 'file' not in request.files:
            return {'error': 'File not provided'}, 400

        file = request.files['file'].read()

        dicom_bytes = DicomBytesIO(file)
        try:
            ds = pydicom.dcmread(dicom_bytes)
        except InvalidDicomError:
            return {'error': 'Invalid DICOM file'}, 400

        ds = self.anonymization_service.anonymize(ds)

        buffer = io.BytesIO()
        memory_dataset = DicomFileLike(buffer)
        pydicom.dcmwrite(memory_dataset, ds)
        memory_dataset.seek(0)

        return send_file(buffer, mimetype='application/dicom')
