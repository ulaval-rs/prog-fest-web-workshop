from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from ..services.data import DataService
from ..services.account import AccountService


class AvailableDataResource(Resource):

    def get(self):
        """
        ---
        tags:
            - Données
        responses:
            200:
                description: Types de données possibles
                type: Array
        """
        return ['sphere', 'cylinder', 'cone', 'dose']


class DataResource(Resource):

    def __init__(self,
                 parser: RequestParser,
                 account_service: AccountService,
                 data_service: DataService):
        self.parser = parser
        self.account_service = account_service
        self.data_service = data_service

    def get(self, data_type):
        """
        ---
        tags:
            - Données
        parameters:
            - in: token
              required: true
            - in: data_type
              required: true
        responses:
            200:
                description: Retourne le fichier en octets (bytes)
            400:
                description: Token absent
            401:
                description: Accès refusé
            404:
                description: Type de données non trouvé

        """
        args = self.parser.parse_args()
        token = args['token']

        if not token:
            return {'error': 'Token not provided'}, 400

        if not self.account_service.is_authorized(token):
            return {'error': 'Not authorized'}, 401

        if data_type == 'dose':
            return self.data_service.retrieve_dose()
        if data_type == 'sphere':
            return self.data_service.retrieve_structure('sphere')
        if data_type == 'cylinder':
            return self.data_service.retrieve_structure('cylinder')
        if data_type == 'cone':
            return self.data_service.retrieve_structure('cone')

        return {'error': f'Data type "{data_type}" not found. Accepted data type are ("structure" or "dose").'}, 404
