from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp

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
