from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Profession as professionModel
from sqlalchemy import asc
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

class ProfessionList(Resource):
    @jwt_required
    def get(self):
        allPr = [{'id': pr.id, 'name': pr.name} for pr in professionModel.query.all()]
        return allPr

class Profession(Resource):
    @jwt_required
    def get(self, id):
        pr = professionModel.query.get(id)
        if pr:
            return{
                'id': pr.id,
                'name': pr.name
            }
    
    @jwt_required
    def post(self):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None


        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        pr = professionModel(name=name)
        db.session.add(pr)
        db.session.commit()
    @jwt_required
    def patch(self, id):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        pr = professionModel.query.get(id)

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        if pr:
            pr.name = name
            db.session.commit()

        allPr = [{'id': x.id, 'name':x.name} for x in professionModel.query.order_by(asc(professionModel.id))]

        return allPr


    @jwt_required
    def delete(self, id):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        pr = professionModel.query.get(id)
        if pr:
            db.session.delete(pr)
            db.session.commit()

        allPr = [{'id': x.id, 'name':x.name} for x in professionModel.query.order_by(asc(professionModel.id))]

        return allPr