from flask import send_file

from web_app.dao import Dao


class DataService:

    def __init__(self, dao: Dao):
        self.dao = dao

    def retrieve_dose(self):
        dose_path = self.dao.retrieve_path('rtdose')

        return send_file(dose_path)

    def retrieve_structure(self, structure: str = 'rtstruct-sphere'):
        structure_path = self.dao.retrieve_path(structure)

        return send_file(structure_path)
