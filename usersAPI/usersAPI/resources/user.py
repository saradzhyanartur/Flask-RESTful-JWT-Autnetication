from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    get_jti,
)
from marshmallow import ValidationError

from usersAPI.schemas.users import UserSchema
from usersAPI.models.user import UserModel
from usersAPI import bcrypt, revoked_store
from usersAPI.config import ACCESS_EXPIRES, REFRESH_EXPIRES

user_schema = UserSchema()

class User(Resource):
    '''This resource is implemented for testing purposes. It is recommended that you 
        remove it before production or amend the scope of the access.'''
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200

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
            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
            revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)
            print(revoked_store.get(access_token))
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid Credentials'}, 401

class AccessTokenRevoke(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti'] #jti is unique id for the token
        revoked_store.set(jti, 'true', ACCESS_EXPIRES * 1.2)
        return {"msg": "Access token revoked"}, 200

class RefreshTokenRevoke(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true', REFRESH_EXPIRES * 1.2)
        return {"msg": "Refresh token revoked"}, 200

class AccessTokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        access_jti = get_jti(encoded_token=new_token)
        revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        return {'access_token': new_token}, 200