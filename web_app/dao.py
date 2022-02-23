import os


class Dao:

    def __init__(self, data_path: str):
        self._data_path = data_path

        self.users = {}
        self._data = {}

        self._load_data()

    def retrieve_path(self, data_object: str) -> str:
        return self._data[data_object]

    def _load_data(self):
        for filename in os.listdir(self._data_path):
            path = os.path.join(self._data_path, filename)

            key, _ = filename.split('.')
            self._data[key] = path
