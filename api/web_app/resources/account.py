from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from web_app.services import AccountService
from web_app.services.account import UserExistsError


class AccountResource(Resource):

    def __init__(self, parser: RequestParser, account_service: AccountService):
        self.parser = parser
        self.account_service = account_service

    def post(self):
        """
        Create account
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

        if not self.account_service.is_idul_valid(idul):
            return {'error': f'Bad IDUL: "{idul}"'}, 400

        try:
            self.account_service.add_user(idul)
        except UserExistsError:
            return {'error': f'"{idul}" user already exits'}, 409

        return {'message': 'created'}, 201
