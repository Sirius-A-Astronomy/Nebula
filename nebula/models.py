from nebula import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    username = db.Column(db.String(128), nullable=False, unique=True)

    # email should just be: username@astro.rug.nl, no need to store it ?

    def __repr__(self):
        return f"User(\"{self.username}\")"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(16), nullable=False, unique=True)
    description = db.Column(db.Text)

    # relation one-to-many: one course_level, many courses
    course_level_id = db.Column(db.Integer,
                                db.ForeignKey('course_level.id'),
                                nullable=False)
    course_level = db.relationship('CourseLevel',
                                   backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f"Course(\"{self.name}\")"


class CourseLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # maybe we need a better name for the CourseLevel.name, as it
    #  referres to the year in which the course if given.
    name = db.Column(db.String(128), nullable=False)
    # maybe there is some kind of enumerate option for this:
    study_type = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"CourseLevel(\"{self.study_type}\", \"{self.name}\")"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    creation_datetime = db.Column(db.DateTime,
                                  nullable=False,
                                  default=datetime.now)
    difficulty = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    sources = db.Column(db.Text)

    # relation one-to-many: one course, many questions
    course_id = db.Column(db.Integer,
                          db.ForeignKey('course.id'),
                          nullable=False)
    course = db.relationship('Course',
                             backref=db.backref('questions', lazy=True))

    # relation one-to-many: one user, many questions
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('questions', lazy=True))

    # the many-to-many relations requires an extra table:
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships
    # TODO relation many-to-many: many: subject_tag, many: questions
    # TODO relation many-to-many: many: type_tag, many: questions

    def __repr__(self):
        return f"Question(\"{self.title}\")"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_suggestion = db.Column(db.Boolean, nullable=False, default=False)

    # relation one-to-many: one: user, many: comments
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    # relation one-to-many: one: question, many: comments
    question_id = db.Column(db.Integer,
                            db.ForeignKey('question.id'),
                            nullable=False)
    question = db.relationship('Question',
                               backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"Comment(\"{self.content}\")"
