from dicompylercore import dvhcalc
from flask import request
from flask_restful import Resource
from pydicom.errors import InvalidDicomError

from web_app.resources import util


class DvhResource(Resource):

    def post(self):
        """
        Calculate DVH
        ---
        tags:
            - Dose
        requestBody:
            content:
                multipart/form-data:
                    schema:
                        type: object
                        properties:
                            file_dose:
                                type: string
                                format: binary
                            file_struct:
                                type: string
                                format: binary
        response:
            200:
                description: DVH
                type: object
                properties:
                    name: string
                    type: string
                    volume: number
                    dose_units: string
                    doses: array
                    volume_units: string
                    volumes: array
        """
        if 'file_dose' not in request.files or 'file_struct' not in request.files:
            return {'error': '"file_dose" or "file_struct" not provided'}, 400

        dose_bytes = request.files['file_dose'].read()
        struct_bytes = request.files['file_struct'].read()

        try:
            rtdose = util.read_dicom_dataset(dose_bytes)
            if rtdose.Modality != 'RTDOSE':
                raise InvalidDicomError

        except InvalidDicomError:
            return {'error': 'Invalid RTDose file'}, 400
        try:
            rtstruct = util.read_dicom_dataset(struct_bytes)
            if rtstruct.Modality != 'RTSTRUCT':
                raise InvalidDicomError

        except InvalidDicomError:
            return {'error': 'Invalid RTStruct file'}, 400

        dvhs = []

        for roi in rtstruct.StructureSetROISequence:
            dvh = dvhcalc.get_dvh(rtstruct, rtdose, roi.ROINumber)

            if len(dvh.bins) != len(dvh.counts):
                dvh.bins = dvh.bins[:-abs(len(dvh.bins) - len(dvh.counts))]

            dvhs.append({
                'name': dvh.name,
                'type': dvh.dvh_type,
                'volume': float(dvh.volume),
                'dose_units': dvh.dose_units,
                'doses': [float(i) for i in dvh.bins],
                'volume_units': dvh.volume_units,
                'volumes': [float(i) for i in dvh.counts]
            })

        return dvhs, 200
