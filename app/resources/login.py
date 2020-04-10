from app import app, api, db
from flask import jsonify
from flask_restful import Api, Resource, reqparse
from app import jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.models import Users
import datetime

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str)
        parser.add_argument('password', type=str)

        login = parser.parse_args()['login']
        password = parser.parse_args()['password']

        user = Users.query.filter_by(login=login).first()

        if user and user.password == password:

            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=login, expires_delta=expires)

            return {
                'role': user.role,
                'token': access_token
            }
        return None

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = Users.query.filter_by(login=identity).first()
    return {
        'role': user.role
    }