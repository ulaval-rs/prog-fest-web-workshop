from flask import Flask
from flask_restful import Api

from wep_app import resources

app = Flask(__name__)
api = Api(app)

# Infrastructure

# Services

# Resources
hello_resource = resources.HelloResource()
# token_resource = resources.TokenResource()

api.add_resource(hello_resource, '/')

if __name__ == '__main__':
    app.run()
