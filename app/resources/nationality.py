from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp
from sqlalchemy import asc
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)


class NationalityList(Resource):
    @jwt_required
    def get(self):
        return getAllNationality()


class Nationality(Resource):
    @jwt_required
    def get(self, id):
        nat = Nat.query.get(id)
        if nat:
            return {
                'name': nat.name
            }
        else:
            return None

    @jwt_required
    def post(self):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        nat = Nat(name=name)
        if not nat.isExist():
            db.session.add(nat)
            db.session.commit()

        return getAllNationality()

    @jwt_required
    def patch(self, id):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        nat = Nat.query.get(id)
        if nat:
            nat.update(name)
        
        return getAllNationality()


    @jwt_required
    def delete(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        nat = Nat.query.get(id)
        if nat:
            nat.delete()

        return getAllNationality()

def getAllNationality():
    nat = Nat.query.order_by(asc(Nat.id)).all()
    allNat = [{'id': n.id, 'name': n.name} for n in nat]
    return allNat