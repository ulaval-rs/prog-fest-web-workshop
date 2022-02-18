from flask import send_file


class DataService:

    def __init__(self, data_path: str):
        self.data_path = data_path

    def retrieve_dose(self):
        return send_file(f'{self.data_path}/rtdose.dcm')

    def retrieve_structure(self):
        return send_file(f'{self.data_path}/rtstruct-sphere.dcm')
