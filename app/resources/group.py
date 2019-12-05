from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp
from sqlalchemy import asc


class Group(Resource):

    def get(self, id):
        gr = Gr.query.get(id)
        if gr:
            return{
                'name': gr.name,
                'speciality': gr.speciality.name if gr.speciality else None,
                'course': gr.course,
                'status': gr.status
            }
        return None

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('speciality_id', type=int)
        parser.add_argument('course', type=int)
        parser.add_argument('status', type=bool)

        name = parser.parse_args()['name']
        speciality_id = parser.parse_args()['speciality_id']
        course = parser.parse_args()['course']
        status = parser.parse_args()['status']

        gr = Gr(name=name, speciality_id=speciality_id,
                course=course, status=status)
        db.session.add(gr)
        db.session.commit()

    def patch(self, id):
        gr = Gr.query.get(id)
        if not gr:
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('speciality_id', type=int)
        parser.add_argument('course', type=int)
        parser.add_argument('status', type=bool)

        name = parser.parse_args()['name']
        speciality_id = parser.parse_args()['speciality_id']
        course = parser.parse_args()['course']
        status = parser.parse_args()['status']

        gr.update(name=name, speciality_id=speciality_id,
                  course=course, status=status)

        return getAllGroup()

    def delete(self, id):
        gr = Gr.query.get(id)
        if not gr:
            return None
        print(ok)
        # gr.delete()


class GroupList(Resource):

    def get(self):
        return getAllGroup()

def getAllGroup():
    gr = Gr.query.order_by(asc(Gr.id)).all()
    if gr:
        grList = []
        for item in gr:
            grList.append({
                'id': item.id,
                'name': item.name,
                'speciality': item.speciality.name if item.speciality else None,
                'course': item.course,
                'status': item.status
            })
        return grList
    return None