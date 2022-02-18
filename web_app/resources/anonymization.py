from flask import request, send_file
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from pydicom.errors import InvalidDicomError

from web_app import services
from web_app.resources import util


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
        requestBody:
            content:
                multipart/form-data:
                    schema:
                        type: object
                        properties:
                            file:
                                type: string
                                format: binary
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

        file_bytes = request.files['file'].read()

        try:
            ds = util.read_dicom_dataset(file_bytes)
        except InvalidDicomError:
            return {'error': 'Invalid DICOM file'}, 400

        ds = self.anonymization_service.anonymize(ds)

        dicom_bytes_io = util.dicom_dataset_to_bytes(ds)

        return send_file(dicom_bytes_io, mimetype='application/dicom')
