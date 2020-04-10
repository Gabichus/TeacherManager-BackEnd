from app import db


class Nationality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    teacher = db.relationship('Teacher', backref='nationality', lazy='dynamic')

    def update(self, name):
        self.name = name
        db.session.commit()

    def getTeacher(self):
        teacher = self.teacher.all()
        return teacher

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def isExist(self):
        status = True if Nationality.query.filter_by(name=self.name).first() else False
        return status


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    patronymic = db.Column(db.String(64))
    sex = db.Column(db.Boolean)
    birthDate = db.Column(db.DateTime)
    birthPlace = db.Column(db.String(64))
    familyStatus = db.Column(db.Boolean)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    address = db.Column(db.String(64))
    idnp = db.Column(db.String(64), unique=True)
    series = db.Column(db.String(64))
    nr = db.Column(db.String(64))
    officeGive = db.Column(db.String(64))
    dateGive = db.Column(db.DateTime)
    nationality_id = db.Column(db.Integer, db.ForeignKey('nationality.id'))
    email = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    speciality_id = db.Column(db.Integer, db.ForeignKey('speciality.id'))
    profession_id = db.Column(db.Integer, db.ForeignKey('profession.id'))
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'))
    nr_stage_years = db.Column(db.Integer)
    paid = db.Column(db.Boolean)
    filesPath = db.relationship('filePath', backref='region', lazy='dynamic')

    def __repr__(self):
        return '<name {} nationality {}>'.format(self.name, self.nationality_id)

    def getGroup(self):
        return self.group

    def update(self):
        pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()    


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speciality_id = db.Column(db.Integer, db.ForeignKey('speciality.id'))
    name = db.Column(db.String(64))
    course = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    teacher = db.relationship('Teacher', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<name {}>'.format(self.name)

    def getTeacher(self):
        return self.teacher.all()

    def getSpeciality(self):
        return self.speciality

    def update(self, name, speciality_id, course, status):
        if name is not None:
            self.name = name
        if speciality_id is not None:
            self.speciality_id = speciality_id
        if course is not None:
            self.course = course
        if status is not None:
            self.status = status
        
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Speciality(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    nr_study_years = db.Column(db.Integer)
    nr_credits = db.Column(db.Integer)
    english = db.Column(db.String(64))
    teacher = db.relationship('Teacher', backref='speciality', lazy='dynamic')
    group = db.relationship('Group', backref='speciality', lazy='dynamic')

    def __repr__(self):
        return '<name {}>'.format(self.name)

    def getTeacher(self):
        return self.teacher.all()

    def getGroup(self):
        return self.group.all()

    def update(self, name, nrYears, nrCredits, english):
        if name:
            self.name = name
        if nrYears:
            self.nr_study_years = nrYears
        if nrCredits:
            self.nr_credits = nrCredits
            print(nrCredits)
        if english:
            self.english = english
            print(english)

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    teacher = db.relationship('Teacher', backref='profession', lazy='dynamic')


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    teacher = db.relationship('Teacher', backref='grade', lazy='dynamic')


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    teacher = db.relationship('Teacher', backref='region', lazy='dynamic')

class filePath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    path = db.Column(db.String)
    fileType = db.Column(db.String(64))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64))
    password = db.Column(db.String(64))
    role = db.Column(db.String(64))
    