from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp, Grade as gradeModel
from sqlalchemy import asc, and_, extract, func
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)


class TeacherList(Resource):
    @jwt_required
    def get(self):
        tc = Tc.query.order_by(asc(Tc.id)).all()
        allTc = [minTeacherJson(x) for x in tc]
        return allTc


class Teacher(Resource):
    @jwt_required
    def get(self, id):
        tc = Tc.query.get(id)
        if not tc:
            return None

        tcJson = teacherJson(tc)

        tcJson['files'] = [{'id': x.id, 'name': x.name} for x in tc.filesPath]

        return tcJson
    @jwt_required
    def post(self):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None


        # region parser
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('patronymic', type=str)
        parser.add_argument('sex', type=bool)
        parser.add_argument('birthDate')
        parser.add_argument('birthPlace', type=str)
        parser.add_argument('familyStatus', type=bool)
        parser.add_argument('address', type=str)
        parser.add_argument('idnp', type=str)
        parser.add_argument('series', type=str)
        parser.add_argument('nr', type=str)
        parser.add_argument('officeGive', type=str)
        parser.add_argument('dateGive')
        parser.add_argument('nationality_id', type=int)
        parser.add_argument('email', type=str)
        parser.add_argument('group_id', type=int)
        parser.add_argument('speciality_id', type=int)
        parser.add_argument('nr_stage_years', type=int)
        parser.add_argument('region_id', type=int)
        parser.add_argument('paid', type=bool)

        name = parser.parse_args()['name']
        surname = parser.parse_args()['surname']
        patronymic = parser.parse_args()['patronymic']
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
        nr_stage_years = parser.parse_args()['nr_stage_years']
        paid = parser.parse_args()['paid']
        region_id = parser.parse_args()['region_id']
        
        grade = gradeModel.query.filter(gradeModel.name.ilike('fara grad')).first()

        # endregion

        newTc = Tc(
            name=name,
            surname=surname,
            patronymic=patronymic,
            birthDate=birthDate,
            birthPlace=birtPlace,
            familyStatus=familyStatus,
            address=address,
            idnp=idnp,
            series=series,
            nr=nr,
            officeGive=officeGive,
            dateGive=dateGive,
            nationality_id=nationality_id,
            email=email,
            group_id=group_id,
            speciality_id=speciality_id,
            grade_id = grade.id if grade else None,
            region_id = region_id,
            nr_stage_years = nr_stage_years
        )

        db.session.add(newTc)
        db.session.commit()

        tc = Tc.query.order_by(asc(Tc.id)).all()
        allTc = [minTeacherJson(x) for x in tc]
        return allTc
    @jwt_required
    def patch(self, id):
        
        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        tc = Tc.query.get(id)
        if not tc:
            return None

        #region parser
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('patronymic', type=str)
        parser.add_argument('sex', type=bool)
        parser.add_argument('birthDate')
        parser.add_argument('birthPlace', type=str)
        parser.add_argument('familyStatus', type=bool)
        parser.add_argument('address', type=str)
        parser.add_argument('idnp', type=str)
        parser.add_argument('series', type=str)
        parser.add_argument('nr', type=str)
        parser.add_argument('officeGive', type=str)
        parser.add_argument('dateGive')
        parser.add_argument('nationality_id', type=int)
        parser.add_argument('email', type=str)
        parser.add_argument('group_id', type=int)
        parser.add_argument('speciality_id', type=int)
        parser.add_argument('profession_id', type=int)
        parser.add_argument('grade_id', type=int)
        parser.add_argument('nr_stage_years', type=int)
        parser.add_argument('paid', type=bool)
        parser.add_argument('region_id', type=int)

        name = parser.parse_args()['name']
        surname = parser.parse_args()['surname']
        patronymic = parser.parse_args()['patronymic']
        birthDate = parser.parse_args()['birthDate']
        birthPlace = parser.parse_args()['birthPlace']
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
        profession_id = parser.parse_args()['profession_id']
        grade_id = parser.parse_args()['grade_id']
        nr_stage_years = parser.parse_args()['nr_stage_years']
        paid = parser.parse_args()['paid']
        region_id = parser.parse_args()['region_id']
        # endregion

        #region update
        if name:
            tc.name = name
        if surname:
            tc.surname = surname
        if patronymic:
            tc.patronymic = patronymic
        if birthDate:
            tc.birthDate = birthDate
        if birthPlace:
            tc.birthPlace = birthPlace
        if familyStatus:
            tc.familyStatus = familyStatus
        if address:
            tc.address = address
        if idnp:
            tc.idnp = idnp
        if series:
            tc.series = series
        if nr:
            tc.nr = nr
        if officeGive:
            tc.officeGive = officeGive
        if dateGive:
            tc.dateGive = dateGive
        if nationality_id:
            tc.nationality_id = nationality_id
        if email:
            tc.email = email
        if group_id:
            tc.group_id = group_id
        if speciality_id:
            tc.speciality_id = speciality_id
        if profession_id:
            tc.profession_id = profession_id
        if grade_id:
            tc.grade_id = grade_id
        if nr_stage_years:
            tc.nr_stage_years = nr_stage_years
        if paid is not None:
            tc.paid = paid
        if region_id:
            tc.region_id=region_id
            

        db.session.commit()

        #endregion

        tc = Tc.query.order_by(asc(Tc.id)).all()
        allTc = [minTeacherJson(x) for x in tc]
        return allTc

    @jwt_required
    def delete(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        tc = Tc.query.get(id)
        if tc:
            tc.delete()

        tc = Tc.query.order_by(asc(Tc.id)).all()
        allTc = [minTeacherJson(x) for x in tc]
        return allTc


class TeacherPaid(Resource):
    @jwt_required
    def get(self):
        AllGroups = []
        groups = Gr.query.filter(and_(Gr.status==True, Gr.teacher != None)).all()
        for gr in groups:
            teacherGroup = gr.teacher.filter_by(paid=False).all()
            allTeacher = [teacherJson(x) for x in teacherGroup]
            AllGroups.append({'group': gr.name, 'speciality':gr.speciality.name if gr.speciality else None ,'teachers':allTeacher})
        return AllGroups


class TeacherAge(Resource):
    @jwt_required
    def get(self,min,max):
        
        tc = Tc.query.order_by(asc(Tc.birthDate)).filter(and_(2020-extract('year', Tc.birthDate) > min),2020-extract('year', Tc.birthDate) < max).all()
        allTc = [teacherJson(x) for x in tc]
        return allTc


class TeacherStage(Resource):
    @jwt_required
    def get(self,min,max):
        tc = Tc.query.filter(Tc.nr_stage_years>min, Tc.nr_stage_years<max).all()
        allTc = [teacherJson(x) for x in tc]
        return allTc


def teacherJson(tc):
    return{
        'id': tc.id,
        'name': tc.name,
        'surname': tc.surname,
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
        'group_id': tc.group.name if tc.group_id else None,
        'speciality_id': tc.speciality.name if tc.speciality_id else None,
        'grade': tc.grade.name if tc.grade else None,
        'profession': tc.profession.name if tc.profession else None,
        'paid': tc.paid,
        'region': tc.region.name if tc.region else None,
        'nr_stage_years': tc.nr_stage_years
    }


def minTeacherJson(tc):
    return{
        'id': tc.id,
        'name': tc.name,
        'surname': tc.surname,
        'patronymic': tc.patronymic,
        'group': tc.group.name if tc.group else None,
        'speciality': tc.speciality.name if tc.speciality else None,
        'grade': tc.grade.name if tc.grade else None,
        'profession': tc.profession.name if tc.profession else None
    }
