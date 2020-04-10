from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Grade as gradeModel
from sqlalchemy import asc
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

class GradeList(Resource):
    def get(self):
        gr = gradeModel.query.all()
        allGr = [{'id': g.id, "name":g.name} for g in gr]
        return allGr


class Grade(Resource):
    @jwt_required
    def get(self, id):
        gr = gradeModel.query.get(id)

        if gr:
            return{
                'id':gr.id,
                'name':gr.name
            }

    @jwt_required
    def post(self):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        gr = gradeModel(name = name)
        db.session.add(gr)
        db.session.commit()
        
    @jwt_required
    def patch(self, id):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        gr = gradeModel.query.get(id)

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        if gr:
            gr.name = name
            db.session.commit()

        allGr = [{'id': x.id, 'name':x.name} for x in gradeModel.query.order_by(asc(gradeModel.id))]

        return allGr

    @jwt_required
    def delete(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        gr = gradeModel.query.get(id)
        if not gr:
            return None

        db.session.delete(gr)
        db.session.commit()

        allGr = [{'id': x.id, 'name':x.name} for x in gradeModel.query.order_by(asc(gradeModel.id))]

        return allGr
