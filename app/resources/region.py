from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Region as regionModel, Teacher as Tc
from app.resources.teacher import teacherJson
from sqlalchemy import asc
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

class RegionList(Resource):
    @jwt_required
    def get(self):
        allReg = [{'id': reg.id, 'name': reg.name} for reg in regionModel.query.all()]
        return allReg

class Region(Resource):
    @jwt_required
    def get(self,id):
        reg = regionModel.query.get(id)
        if reg:
            return {'id': reg.id, 'name': reg.name}

    @jwt_required
    def post(self):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        reg = regionModel(name=name)
        db.session.add(reg)
        db.session.commit()

    @jwt_required
    def patch(self, id):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        reg = regionModel.query.get(id)

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        if reg:
            reg.name = name
            db.session.commit()

        allReg = [{'id': x.id, 'name':x.name} for x in regionModel.query.order_by(asc(regionModel.id))]

        return allReg

    @jwt_required
    def delete(self, id):
        
        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        reg = regionModel.query.get(id)
        if reg:
            db.session.delete(reg)
            db.session.commit()

        allReg = [{'id': x.id, 'name':x.name} for x in regionModel.query.order_by(asc(regionModel.id))]

        return allReg


class RegionTeacher(Resource):
    @jwt_required
    def get(self,id):
        reg = regionModel.query.get(id)
        if not reg:
            return None

        allTeacher = [teacherJson(x) for x in reg.teacher]
        return allTeacher