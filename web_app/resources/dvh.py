import io
from typing import Dict, List

import matplotlib.pyplot as plt
from dicompylercore import dvhcalc
from flask import request, send_file
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


class DvhPlotterResource(Resource):

    def post(self):
        dvhs = request.json['dvhs']

        if not self._is_dvhs_valid(dvhs):
            return {'error': f'Invalid DVHs'}, 400

        self._make_volume_relative(dvhs)

        for dvh in dvhs:
            plt.plot(dvh['doses'], dvh['volumes'], label=dvh['name'])

        plt.legend()
        plt.xlabel(f'Dose [{dvhs[0]["dose_units"]}]')
        plt.ylabel(f'Volume [{dvhs[0]["volume_units"]}]')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.clf()
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')

    def _is_dvhs_valid(self, dvhs: List[Dict]) -> bool:
        dose_units, volume_units = set(), set()

        if not isinstance(dvhs, list):
            return False

        for dvh in dvhs:
            if ('name' not in dvh or 'volumes' not in dvh or 'doses' not in dvh or
                    'volume_units' not in dvh or 'dose_units' not in dvh):
                return False

            if len(dvh['volumes']) != len(dvh['doses']):
                return False

            dose_units.add(dvh['dose_units'])
            volume_units.add(dvh['volume_units'])

        if len(dose_units) != 1 or len(volume_units) != 1:
            return False

        return True

    def _make_volume_relative(self, dvhs: List[Dict]):
        for dvh in dvhs:
            max_volume = max(dvh['volumes'])
            dvh['volumes'] = [v / max_volume * 100 for v in dvh['volumes']]
            dvh['volume_units'] = '%'
