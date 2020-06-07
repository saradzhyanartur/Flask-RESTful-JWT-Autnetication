from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from usersAPI.blacklist import BLACKLIST
from usersAPI.config import Config
from usersAPI.authentication import jwt


db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api()

def create_app(config_class: 'Config' = Config) -> 'app':
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    import usersAPI.endpoints as endpoints
    for endpoint in endpoints.exposed:
        api.add_resource(endpoint.resource, endpoint.path)
    api.init_app(app)

    return app

