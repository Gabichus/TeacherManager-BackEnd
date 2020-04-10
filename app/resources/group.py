from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp
from app.resources.teacher import minTeacherJson, teacherJson
from sqlalchemy import asc
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)


class Group(Resource):
    @jwt_required
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

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('speciality_id', type=int)
        # parser.add_argument('course', type=int)
        # parser.add_argument('status', type=bool)

        name = parser.parse_args()['name']
        speciality_id = parser.parse_args()['speciality_id']
        # course = parser.parse_args()['course']
        # status = parser.parse_args()['status']

        gr = Gr(name=name, speciality_id=speciality_id,
                course=1, status=False)
        db.session.add(gr)
        db.session.commit()

        return getAllGroup()
    @jwt_required
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
    @jwt_required
    def delete(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        gr = Gr.query.get(id)
        if not gr:
            return None

        gr.delete()

        return getAllGroup()


class GroupList(Resource):

    def get(self):
        return getAllGroup()


class GroupMin(Resource):
    def get(self):
        gr = Gr.query.order_by(asc(Gr.id)).all()
        if gr:
            allGr = [{'id': x.id, 'name': x.name} for x in gr]
            return allGr
        return None


class TeacherOfGroup(Resource):

    def get(self, id):
        gr = Gr.query.get(id)
        if gr:
            allTc = [teacherJson(x) for x in gr.teacher]
            return allTc
        return None


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
