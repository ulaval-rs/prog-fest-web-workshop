from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from ..services import AccountService
from ..services.account import UserDoesNotExistError


class AuthenticationResource(Resource):

    def __init__(self, parser: RequestParser, account_service: AccountService):
        self.parser = parser
        self.account_service = account_service

    def post(self):
        """
        Authenticate
        ---
        tags:
            - Compte
        parameters:
        - in: idul
          name: idul
          required: true
        responses:
            201:
                description: Authentifié
            400:
                description: IDUL invalide ou non fournie
        """
        args = self.parser.parse_args()
        idul = args['idul']

        if not idul:
            return {'error': 'IDUL not provided'}, 400

        try:
            token = self.account_service.retrieve_token(idul)
        except UserDoesNotExistError:
            return {'error': f'No account "{idul}".'}, 404

        return {'token': token}, 200
