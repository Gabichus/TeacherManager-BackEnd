from app import api
from app.resources.group import Group, GroupList
from app.resources.nationality import Nationality, NationalityList
from app.resources.speciality import Speciality, SpecialityList
from app.resources.teacher import Teacher


api.add_resource(NationalityList,  '/nationality')


api.add_resource(Nationality,  '/nationality', '/nationality/<int:id>')


api.add_resource(GroupList, '/group')


api.add_resource(Group, '/group/<int:id>', '/group')


api.add_resource(SpecialityList, '/speciality')


api.add_resource(Speciality, '/speciality/<int:id>', '/speciality')


api.add_resource(Teacher, '/teacher/<int:id>', '/teacher')
