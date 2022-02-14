from .resource import APIResource


class HelloResource(APIResource):

    def __init__(self):
        pass

    def get(self):
        return {'message': "Bonjour et bienvenue au workshop sur le Web!"}
