from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from ..services import AccountService


class AccountResource(Resource):

    def __init__(self, parser: RequestParser, account_service: AccountService):
        self.parser = parser
        self.account_service = account_service

    def post(self):
        args = self.parser.parse_args()

        if not args['idul']:
            return {'error': 'IDUL not provided'}, 400

        if not self.account_service.is_idul_valid(args['idul']):
            return {'error': f'Bad IDUL: "{args["idul"]}"'}, 400

        token = self.account_service.make_new_account(args['idul'])
        return {'token': token}, 201
