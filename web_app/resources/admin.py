from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from web_app.services.admin import AdminService


class AdminResource(Resource):

    def __init__(self, parser: RequestParser, admin_service: AdminService):
        self.parser = parser
        self.admin_service = admin_service

    def post(self):
        args = self.parser.parse_args()
        token = args['token']

        if not token:
            return {'error': 'Token not provided'}, 400

        if self.admin_service.is_admin(token):
            self.admin_service.reset_users()

            return {'message': 'Users reset'}, 200

        return {'error': 'Not authorized'}, 401
