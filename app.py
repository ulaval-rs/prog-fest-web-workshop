from flask import Flask
from flask_restful import Api, reqparse

from wep_app import resources, services, constants

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('idul', type=str, help='Votre IDUL')
parser.add_argument('token', type=str, help='Votre token')
parser.add_argument('structure', type=str, help='Structure (cone, sphere or cylinder)')

# Infrastructure

# Services
token_service = services.TokenService(constants.TOKEN_PREFIX)
authentication_service = services.AuthenticationService(token_service)
data_service = services.DataService(constants.DATA_PATH)

# Resources
api.add_resource(resources.HelloResource, '/')
api.add_resource(
    resources.AuthenticationResource,
    '/auth',
    resource_class_kwargs={'parser': parser, 'authentication_service': authentication_service}
)
api.add_resource(resources.AvailableDataResource, '/data')
api.add_resource(
    resources.DataResource,
    '/data/<data_type>',
    resource_class_kwargs={
        'parser': parser,
        'authentication_service': authentication_service,
        'data_service': data_service
    }
)

if __name__ == '__main__':
    app.run()
