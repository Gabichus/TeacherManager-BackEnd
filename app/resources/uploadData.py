from app import app, api, db
from flask_restful import Api, Resource, reqparse
from app.models import Teacher as Tc, Nationality as Nat, Group as Gr, Speciality as Sp, Grade as gradeModel, filePath as fp
from sqlalchemy import asc, and_, extract, func
from app.resources.teacher import teacherJson
import base64
import random
import string
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

class attachFile(Resource):
    @jwt_required
    def get(self,id):
        getFile = fp.query.get(id)
        if getFile:
            name = getFile.name
            fileType = getFile.fileType
            with open(getFile.path,"rb") as f:
                base64File = base64.b64encode(f.read()).decode('utf-8')
            return{
                'name':name,
                'fileType':fileType,
                'data': base64File
            }

    @jwt_required
    def post(self,id):

        claims = get_jwt_claims()

        if not (claims['role'] == 'admin' or claims['role'] == 'moderator'):
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('fileType', type=str)

        data = parser.parse_args()['data']
        name = parser.parse_args()['name']
        fileType = parser.parse_args()['fileType']

        

        teacher = Tc.query.get(id)
        if teacher:
            try:
                file_content=base64.b64decode(data.replace(' ','+'))
                
                name = name+'_'+''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(4)])
                filePath = "app/static/teacherFile/{}.{}".format(name,fileType)
                with open(filePath,"wb") as f:
                    f.write(file_content)

                newFile = fp(name=name, path=filePath, teacher_id=int(id), fileType=fileType)
                db.session.add(newFile)
                db.session.commit()
            except Exception as e:
                print(str(e))

            tc = Tc.query.get(id)
            tcJson = teacherJson(tc)
            tcJson['files'] = [{'id': x.id, 'name': x.name} for x in tc.filesPath]
            return tcJson
    
    @jwt_required
    def delete(self, id):

        claims = get_jwt_claims()

        if claims['role'] != 'admin':
            return None

        deleteFile = fp.query.get(id)
        if deleteFile:
            db.session.delete(deleteFile)
            db.session.commit()
            tc = Tc.query.get(deleteFile.teacher_id)
            tcJson = teacherJson(tc)
            tcJson['files'] = [{'id': x.id, 'name': x.name} for x in tc.filesPath]
            return tcJson