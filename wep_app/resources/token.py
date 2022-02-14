from .resource import APIResource


class TokenResource(APIResource):

    def __init__(self):
        pass

    def get(self):
        return {'token', None}
