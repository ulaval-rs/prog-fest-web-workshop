from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from ..services.data import DataService
from ..services.authentication import AuthenticationService


class AvailableDataResource(Resource):

    def __init__(self,
                 parser: RequestParser,
                 authentication_service: AuthenticationService,
                 data_service: DataService):
        pass


class DataResource(Resource):

    def __init__(self,
                 parser: RequestParser,
                 authentication_service: AuthenticationService,
                 data_service: DataService):
        self.parser = parser
        self.auth_service = authentication_service
        self.data_service = data_service

    def get(self, data_type):
        args = self.parser.parse_args()
        token = args['token']

        if not token:
            return {'error': 'Token not provided'}, 400

        if not self.auth_service.is_authorized(token):
            return {'error': 'Not authorized'}, 401

        if data_type == 'dose':
            return self.data_service.retrieve_dose()

        if data_type == 'structure':
            return self.data_service.retrieve_structure()

        return {'error': f'Data type "{data_type}" not found. Accepted data type are ("structure" or "dose").'}, 404
