from app import app, db
from app.models import Group, Teacher, Nationality, Speciality

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Group':Group, 'Teacher':Teacher, 'Nationality':Nationality, 'Speciality':Speciality}