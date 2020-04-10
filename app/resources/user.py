from app import app, api, db
from flask import jsonify
from flask_restful import Api, Resource, reqparse
from app.models import Users
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

class manageUser(Resource):
    @jwt_required
    def get(self):
        
        identity = get_jwt_identity()

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        user = [{'id': x.id,'login':x.login,'role': x.role} for x in Users.query.all() if x.login != identity]
        return user

    @jwt_required
    def post(self):

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('role', type=str)

        login = parser.parse_args()['login']
        password = parser.parse_args()['password']
        role = parser.parse_args()['role']

        newUser = Users(login=login, password=password, role=role)

        db.session.add(newUser)
        db.session.commit()

        identity = get_jwt_identity()

        user = [{'id':x.id, 'login':x.login,'role': x.role} for x in Users.query.all() if x.login != identity]
        return user

    @jwt_required
    def patch(self,id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        parser.add_argument('role', type=str)

        password = parser.parse_args()['password']
        role = parser.parse_args()['role']

        user = Users.query.get(id)

        if user:
            if password:
                user.password = password
            if role:
                user.role = role

        db.session.commit()

        identity = get_jwt_identity()

        user = [{'id':x.id, 'login':x.login,'role': x.role} for x in Users.query.all() if x.login != identity]
        return user

    @jwt_required
    def delete(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        user = Users.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()   

            identity = get_jwt_identity()

            user = [{'id':x.id, 'login':x.login,'role': x.role} for x in Users.query.all() if x.login != identity]
            return user     

