from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import redis

db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api()
revoked_store = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
#print('Revoked Store ID: ', id(revoked_store))

from usersAPI.config import Config
from usersAPI.authentication import jwt

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app) 
    bcrypt.init_app(app)
    jwt.init_app(app)

    import usersAPI.endpoints as endpoints
    for endpoint in endpoints.exposed:
        api.add_resource(endpoint.resource, endpoint.path)
    api.init_app(app)

    with app.app_context():
        db.create_all()

    return app

