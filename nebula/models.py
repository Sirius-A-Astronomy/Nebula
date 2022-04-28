from nebula import db
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(GUID(), primary_key=False,
                     default=lambda: str(uuid.uuid4()))

    # Database uses utc time
    created_at = db.Column(DateTime(timezone=True),
                           server_default=func.utcnow())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.utcnow())


class User(Base):
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    username = db.Column(db.String(128), nullable=False, unique=True)

    # email should just be: username@astro.rug.nl, no need to store it ?

    def __repr__(self):
        return f"User(\"{self.username}\")"


class Course(Base):
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(16), nullable=False, unique=True)
    semester = db.Column(db.String(16))
    description = db.Column(db.Text)

    # relation one-to-many: one course_level, many courses
    course_level_id = db.Column(db.Integer,
                                db.ForeignKey('course_level.id'),
                                nullable=False)
    course_level = db.relationship('CourseLevel',
                                   backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f"Course(\"{self.name}\")"


class CourseLevel(Base):
    # maybe we need a better name for the CourseLevel.name, as it
    #  referres to the year in which the course if given.
    name = db.Column(db.String(128), nullable=False)
    # maybe there is some kind of enumerate option for this:
    study_type = db.Column(db.String(64), nullable=False)
    code = db.Column(db.String(16), nullable=False, unique=True)

    def __repr__(self):
        return f"CourseLevel(\"{self.study_type}\", \"{self.name}\")"


class Question(Base):
    title = db.Column(db.String(256), nullable=False)
    difficulty = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=False)
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


class Comment(Base):
    content = db.Column(db.Text, nullable=False)
    is_suggestion = db.Column(db.Boolean, nullable=False, default=False)
    # creation_datetime = db.Column(
    #     db.DateTime, nullable=True, default=datetime.now)

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


def init_db():
    db.create_all()
