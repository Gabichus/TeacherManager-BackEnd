from app import api
from app.resources.group import Group, GroupList, GroupMin, TeacherOfGroup
from app.resources.nationality import Nationality, NationalityList
from app.resources.speciality import Speciality, SpecialityList, SpecialityMin, GroupOfSpeciality
from app.resources.teacher import Teacher, TeacherList, TeacherPaid, TeacherAge, TeacherStage
from app.resources.grade import Grade, GradeList
from app.resources.profession import Profession, ProfessionList
from app.resources.region import Region, RegionList, RegionTeacher
from app.resources.uploadData import attachFile
from app.resources.login import Login
from app.resources.user import manageUser
# region Nationality
api.add_resource(NationalityList,  '/nationality')

api.add_resource(Nationality,  '/nationality', '/nationality/<int:id>')

# endregion

# region Group

api.add_resource(GroupList, '/group')

api.add_resource(Group, '/group/<int:id>', '/group')

api.add_resource(GroupMin, '/groupMin')

api.add_resource(TeacherOfGroup, '/teacherGroup/<int:id>')

# endregion

# region Speciality

api.add_resource(SpecialityList, '/speciality')

api.add_resource(Speciality, '/speciality/<int:id>', '/speciality')

api.add_resource(SpecialityMin, '/specialityMin')

api.add_resource(GroupOfSpeciality, '/groupSpeciality/<int:id>')

# endregion

# region Teacher

api.add_resource(TeacherList, '/teacher')

api.add_resource(Teacher, '/teacher/<int:id>', '/teacher')

api.add_resource(TeacherPaid, '/teacherPaid')

api.add_resource(TeacherAge, '/teacherAge/<int:min>/<int:max>')

api.add_resource(TeacherStage, '/teacherStage/<int:min>/<int:max>')

# endregion

# region Grade
api.add_resource(GradeList, '/grade')
api.add_resource(Grade, '/grade/<int:id>', '/grade')
# endregion 

# region Profession
api.add_resource(ProfessionList, '/profession')
api.add_resource(Profession, '/profession/<int:id>', '/profession')
# endregion 

api.add_resource(RegionList, '/region')
api.add_resource(Region, '/region/<int:id>', '/region')
api.add_resource(RegionTeacher, '/regionTeacher/<int:id>')


api.add_resource(attachFile, '/attachFile/<int:id>')


api.add_resource(Login, '/login')

api.add_resource(manageUser, '/user', '/user/<int:id>')



