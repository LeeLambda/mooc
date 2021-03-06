import os.path

from flask.ext.script import Manager, Server

from develop_tools.clean import clean as cln
from develop_tools.pep8 import pep8
from mooc.app import create_app
from mooc.app import db


app_root = os.path.dirname(os.path.realpath(__name__))
conf = 'development.conf'

application = create_app('mooc', os.path.join(app_root, conf))
server = Server(port=13800)
manager = Manager(application)
manager.add_command("runserver", server)


@manager.command
def clean():
    cln()


@manager.command
def check():
    pep8()


@manager.command
def createdb():
    with application.test_request_context():
        # import all Models here
        from mooc.account.model import User, SzuAccount, College, Teacher
        from mooc.course.model import (Subject, Category, Course, Clip,
                                       LearnRecord, ClipTag, CourseTag,
                                       clip_tags, course_tags)
        from mooc.qa.model import UpDownRecord, Answer, Question
        db.create_all()
    print 'Created Database!'


@manager.command
def initdb():
    with application.test_request_context():
        # Initial data for test
        from fixture import init_db
        init_db()
    print "Initialized Database!"


@manager.command
def syncdb():
    createdb()
    initdb()


if __name__ == '__main__':
    manager.run()
