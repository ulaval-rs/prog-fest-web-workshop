from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from ..services import AuthenticationService


class AuthenticationResource(Resource):

    def __init__(self, parser: RequestParser, authentication_service: AuthenticationService):
        self.parser = parser
        self.authentication_service = authentication_service

    def post(self):
        args = self.parser.parse_args()

        if not args['idul']:
            return {'error': 'IDUL not provided'}, 400

        if not self.authentication_service.is_idul_valid(args['idul']):
            return {'error': f'Bad IDUL: "{args["idul"]}"'}, 400

        token = self.authentication_service.authenticate(args['idul'])

        return {'token': token}, 201
