from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from datetime import timedelta

import os

app_flask = Flask(__name__)
api = Api(app_flask)
jwt = JWTManager(app_flask)

app_flask.config['JWT_SECRET_KEY'] = os.urandom(24)
app_flask.config["JWT_TOKEN_LOCATION"] = ["headers"]
# app_flask.config["JWT_SECRET_KEY"] = os.
# app_flask.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)
app_flask.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=10)