from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp


class NationalityList(Resource):
    def get(self):
        nat = Nat.query.all()
        allNat = [{'id': n.id, 'name': n.name} for n in nat]
        return allNat


class Nationality(Resource):

    def get(self, id):
        nat = Nat.query.get(id)
        if nat:
            return {
                'name': nat.name
            }
        else:
            return None

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        nat = Nat(name=name)
        if not nat.isExist():
            db.session.add(nat)
            db.session.commit()

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        name = parser.parse_args()['name']

        nat = Nat.query.get(id)
        if nat:
            nat.update(name)
        
        return self.get(id)

    def delete(self, id):
        nat = Nat.query.get(id)
        if nat:
            nat.delete()
