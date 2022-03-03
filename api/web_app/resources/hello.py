from flask_restful import Resource


class HelloResource(Resource):

    def get(self):
        """
        Message de bienvenue
        ---
        tags:
            - General
        responses:
            200:
                description: Message de bienvenu
                schema:
                    message: str
        """
        return {'message': "Bonjour et bienvenue à l'atelier sur les API REST!"}
