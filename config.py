import os


postgres = {
    'user': 'gabichus',
    'pw': '123',
    'db': 'TeacherDb',
    'host': 'localhost'
}

class Config(object):
    SECRET_KEY = 'y5225ou-winvhnhnhll-nc ngcnnmnbhever-v cvncguess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s/%(db)s' % postgres
    SQLALCHEMY_TRACK_MODIFICATIONS = False
