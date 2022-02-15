from flask_restful import Resource


class HelloResource(Resource):

    def get(self):
        return {'message': "Bonjour et bienvenue au workshop sur le Web!"}
