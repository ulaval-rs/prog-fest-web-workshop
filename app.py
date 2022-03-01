from flasgger import Swagger
from flask import Flask
from flask_restful import Api, reqparse

from web_app import constants, resources, services
from web_app.dao import Dao

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'Atelier REST API',
}
swag = Swagger(app)

parser = reqparse.RequestParser()
parser.add_argument('idul', type=str, help='Votre IDUL')
parser.add_argument('token', type=str, help='Votre token')
parser.add_argument('structure', type=str, help='Structure')

# Infrastructure
dao = Dao(constants.DATA_PATH)

# Services
token_service = services.TokenService(constants.TOKEN_PREFIX)
account_service = services.AccountService(dao, token_service)
data_service = services.DataService(dao)
anonymization_service = services.AnonymizationService()
admin_service = services.AdminService(dao, token_service)

# Resources
api.add_resource(resources.HelloResource, '/')
api.add_resource(resources.DvhResource, '/dvh')
api.add_resource(resources.DvhPlotterResource, '/dvh/plot')
api.add_resource(resources.AvailableDataResource, '/data')
api.add_resource(
    resources.AccountResource,
    '/account',
    resource_class_kwargs={'parser': parser, 'account_service': account_service}
)
api.add_resource(
    resources.AuthenticationResource,
    '/auth',
    resource_class_kwargs={'parser': parser, 'account_service': account_service}
)
api.add_resource(
    resources.DataResource,
    '/data/<data_type>',
    resource_class_kwargs={'parser': parser, 'account_service': account_service, 'data_service': data_service}
)
api.add_resource(
    resources.AnonymizationResource,
    '/anonymize',
    resource_class_kwargs={'parser': parser, 'anonymization_service': anonymization_service}
)
api.add_resource(
    resources.AdminResource,
    '/admin/reset',
    resource_class_kwargs={'parser': parser, 'admin_service': admin_service}
)

if __name__ == '__main__':
    app.run(threaded=False, processes=1, host='0.0.0.0', port=5000)
