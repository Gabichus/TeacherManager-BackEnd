from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp
from sqlalchemy import asc
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

class SpecialityList(Resource):
    @jwt_required
    def get(self):
       return getAllSpeciality()


class Speciality(Resource):
    @jwt_required
    def get(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin' or claims['role'] != 'moderator':
            return None

        sp = Sp.query.get(id)
        if sp:
            return({
                'id': sp.id,
                'name': sp.name,
                'nrYears': sp.nr_study_years,
                'nrCredits': sp.nr_credits,
                'english': sp.english
            })
        return None

    @jwt_required
    def post(self):

        claims = get_jwt_claims()

        if claims['role'] != 'admin' or claims['role'] != 'moderator':
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('nrYears', type=int)
        parser.add_argument('nrCredits', type=int)
        parser.add_argument('english', type=str)

        name = parser.parse_args()['name']
        nrYears = parser.parse_args()['nrYears']
        nrCredits = parser.parse_args()['nrCredits']
        english = parser.parse_args()['english']

        sp = Sp(name=name, nr_study_years=nrYears,
                nr_credits=nrCredits, english=english)
        db.session.add(sp)
        db.session.commit()

        return getAllSpeciality()

    @jwt_required
    def patch(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin' or claims['role'] != 'moderator':
            return None

        sp = Sp.query.get(id)

        if not sp:
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('nrYears', type=int)
        parser.add_argument('nrCredits', type=int)
        parser.add_argument('english', type=str)

        name = parser.parse_args()['name']
        nrYears = parser.parse_args()['nrYears']
        nrCredits = parser.parse_args()['nrCredits']
        english = parser.parse_args()['english']

        sp.update(name=name, nrYears=nrYears,
                  nrCredits=nrCredits, english=english)

        return getAllSpeciality()

    @jwt_required
    def delete(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin' or claims['role'] != 'moderator':
            return None

        sp = Sp.query.get(id)
        if not sp:
            return None

        sp.delete()

        return getAllSpeciality()


class SpecialityMin(Resource):
    @jwt_required
    def get(self):

        sp = Sp.query.order_by(asc(Sp.id)).all()
        if sp:
            allSp = [{'id':x.id,'name':x.name} for x in sp]
            return allSp
        return None


class GroupOfSpeciality(Resource):

    @jwt_required
    def get(self, id):
        sp = Sp.query.get(id)
        if sp:
            grList = []
            for item in sp.group:
                grList.append({
                    'id': item.id,
                    'name': item.name,
                    'speciality': item.speciality.name if item.speciality else None,
                    'course': item.course,
                    'status': item.status
                })
            return grList
        return None

def getAllSpeciality():
    allSp = Sp.query.order_by(asc(Sp.id)).all()
    if allSp:
        jsonSp = []
        for sp in allSp:
            jsonSp.append({
                'id': sp.id,
                'name': sp.name,
                'nrYears': sp.nr_study_years,
                'nrCredits': sp.nr_credits,
                'english': sp.english
            })
        return jsonSp
    return None
