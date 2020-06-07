from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from marshmellow import ValidationError
from usersAPI.schemas.users import UserSchema
from usersAPI.models.user import UserModel
from usersAPI.blacklist import BLACKLIST
from usersAPI import bcrypt

user_schema = UserSchema()


class UserRegister(Resource):

    @classmethod
    def post(cls):
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        if UserModel.find_by_username(user_data['username']):
            return {"message": "A user with that username already exists"}, 400
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user = UserModel(user_data['username'], hashed_password)
        user.save_to_db()
        return {"message": "User created successfully."}, 201

class User(Resource):
    '''This is a testing resource. It is recommended that you remove it before production or
        reduce the scope to admin only access.'''
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user), 200
        

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200

class UserLogin(Resource):

    @classmethod
    def post(cls):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        user = UserModel.find_by_username(data['username'])
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid Credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] #jti is unique id for the token
        BLACKLIST.add(jti)

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200