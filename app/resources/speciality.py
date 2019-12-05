from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp
from sqlalchemy import asc

class SpecialityList(Resource):

    def get(self):
       return getAllSpeciality()


class Speciality(Resource):

    def get(self, id):

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

    def post(self):
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

    def patch(self, id):
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

    def delete(self, id):
        sp = Sp.query.get(id)
        if not sp:
            return None

        sp.delete()

        return getAllSpeciality()

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