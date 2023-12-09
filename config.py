from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

import os

app_flask = Flask(__name__)
api = Api(app_flask)
jwt = JWTManager(app_flask)

app_flask.config['JWT_SECRET_KEY'] = os.urandom(24)