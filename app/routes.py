from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp
from datetime import datetime


class NationalityList(Resource):
    def get(self):
        nat = Nat.query.all()
        allNat = [{'id': n.id, 'name': n.name} for n in nat]
        return allNat


api.add_resource(NationalityList,  '/nationality')


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

    def delete(self, id):
        nat = Nat.query.get(id)
        if nat:
            nat.delete()


api.add_resource(Nationality,  '/nationality', '/nationality/<int:id>')


class GroupList(Resource):

    def get(self):
        gr = Gr.query.all()
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


api.add_resource(GroupList, '/group')


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

    def delete(self, id):
        gr = Gr.query.get(id)
        if not gr:
            return None

        gr.delete()


api.add_resource(Group, '/group/<int:id>', '/group')


class SpecialityList(Resource):

    def get(self):
        allSp = Sp.query.all()
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


api.add_resource(SpecialityList, '/speciality')


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

    def delete(self, id):
        sp = Sp.query.get(id)
        if not sp:
            return None

        sp.delete()


api.add_resource(Speciality, '/speciality/<int:id>', '/speciality')


class Teacher(Resource):

    def get(self, id):
        tc = Tc.query.get(id)
        if not tc:
            return None

        return teacherJson(tc)

    def post(self):
        # region parser
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('patronymic', type=str)
        parser.add_argument('sex', type=bool)
        parser.add_argument(
            'birthDate', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
        parser.add_argument('birthPlace', type=str)
        parser.add_argument('familyStatus', type=bool)
        parser.add_argument('address', type=str)
        parser.add_argument('idnp', type=str)
        parser.add_argument('series', type=str)
        parser.add_argument('nr', type=str)
        parser.add_argument('officeGive', type=str)
        parser.add_argument(
            'dateGive', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
        parser.add_argument('nationality_id', type=int)
        parser.add_argument('email', type=str)
        parser.add_argument('group_id', type=int)
        parser.add_argument('speciality_id', type=int)

        name = parser.parse_args()['name']
        surname = parser.parse_args()['surname']
        birthDate = parser.parse_args()['birthDate']
        birtPlace = parser.parse_args()['birthPlace']
        familyStatus = parser.parse_args()['familyStatus']
        address = parser.parse_args()['address']
        idnp = parser.parse_args()['idnp']
        series = parser.parse_args()['series']
        nr = parser.parse_args()['nr']
        officeGive = parser.parse_args()['officeGive']
        dateGive = parser.parse_args()['dateGive']
        nationality_id = parser.parse_args()['nationality_id']
        email = parser.parse_args()['email']
        group_id = parser.parse_args()['group_id']
        speciality_id = parser.parse_args()['speciality_id']

        # endregion

        newTc = Tc(
            name=name,
            surname=surname,
            birthDate=birthDate,
            birthPlace=birtPlace,
            familyStatus=familyStatus,
            address=address,
            idnp=idnp,
            serie=series,
            nr=nr,
            officeGive=officeGive,
            dateGive=dateGive,
            nationality_id=nationality_id,
            email=email,
            group_id=group_id,
            speciality_id=speciality_id
        )

        db.session.add(newTc)
        db.session.commit()

    def patch(self, id):
        tc = Tc.query.get(id)
        if not tc:
            return None

        # region parser
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('patronymic', type=str)
        parser.add_argument('sex', type=bool)
        parser.add_argument(
            'birthDate', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
        parser.add_argument('birthPlace', type=str)
        parser.add_argument('familyStatus', type=bool)
        parser.add_argument('address', type=str)
        parser.add_argument('idnp', type=str)
        parser.add_argument('series', type=str)
        parser.add_argument('nr', type=str)
        parser.add_argument('officeGive', type=str)
        parser.add_argument(
            'dateGive', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
        parser.add_argument('nationality_id', type=int)
        parser.add_argument('email', type=str)
        parser.add_argument('group_id', type=int)
        parser.add_argument('speciality_id', type=int)

        name = parser.parse_args()['name']
        surname = parser.parse_args()['surname']
        birthDate = parser.parse_args()['birthDate']
        birtPlace = parser.parse_args()['birthPlace']
        familyStatus = parser.parse_args()['familyStatus']
        address = parser.parse_args()['address']
        idnp = parser.parse_args()['idnp']
        series = parser.parse_args()['series']
        nr = parser.parse_args()['nr']
        officeGive = parser.parse_args()['officeGive']
        dateGive = parser.parse_args()['dateGive']
        nationality_id = parser.parse_args()['nationality_id']
        email = parser.parse_args()['email']
        group_id = parser.parse_args()['group_id']
        speciality_id = parser.parse_args()['speciality_id']

        # endregion

        tc.name = name
        tc.surname = surname
        tc.birthDate = birthDate
        tc.birthPlace = birtPlace
        tc.familyStatus = familyStatus
        tc.address = address
        tc.idnp = idnp
        tc.serie = series
        tc.nr = nr
        tc.officeGive = officeGive
        tc.dateGive = dateGive
        tc.nationality_id = nationality_id
        tc.email = email
        tc.group_id = group_id
        tc.speciality_id = speciality_id

        db.session.commit()

    def delete(self, id):
        tc = Tc.query.get(id)
        if not Tc:
            tc.delete()


api.add_resource(Teacher, '/teacher/<int:id>', '/teacher')


def teacherJson(tc):
    return{
        'id': tc.name,
        'name': tc.surname,
        'patronymic': tc.patronymic,
        'sex': tc.sex,
        'birthDate': str(tc.birthDate) if tc.birthDate else None,
        'birthPlace': tc.birthPlace,
        'familyStatus': tc.familyStatus,
        'address': tc.address,
        'idnp': tc.idnp,
        'series': tc.series,
        'nr': tc.nr,
        'officeGive': tc.officeGive,
        'dateGive': str(tc.dateGive) if tc.dateGive else None,
        'nationality_id': tc.nationality_id,
        'email': tc.email,
        'group_id': tc.group_id.name if tc.group_id else None,
        'speciality_id': tc.speciality_id.name if tc.speciality_id else None
    }
