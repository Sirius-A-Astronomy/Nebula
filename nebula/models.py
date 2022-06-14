import uuid

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy import DateTime, PickleType, func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import UUID

from nebula import db


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
                           server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())


subject_tags = db.Table('subject_tags',
                        db.Column('subject_tag_uuid', GUID(),
                                  db.ForeignKey('subject_tag.uuid')),
                        db.Column('question_uuid', GUID(),
                                  db.ForeignKey('question.uuid'))
                        )


class User(Base):
    """
        User model for the database.

        :param username: The username of the user. Must be unique. Case-insensitive.
        :type username: str
        :param password: The password of the user.
        :type password: str
        :param first_name: The first name of the user.
        :type first_name: str
        :param last_name: The last name of the user.
        :type last_name: str
        :param access_level: The access level of the user.
        :type access_level: int
        :param is_active: Whether the user is active or not.
        :type is_active: bool
        :param is_authenticated: Whether the user is authenticated or not. 
            Is set to true when the user logs in and false when the user logs out.
        :type is_authenticated: bool
        :param is_anonymous: Whether the user is anonymous or not.
        :type is_anonymous: bool

    """
    ACCESS_LEVELS = {
        "guest": 0,
        "user": 1,
        "moderator": 2,
        "admin": 3
    }

    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    username = db.Column(db.String(128), nullable=False, unique=True)
    access_level = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(128), nullable=True)

    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.uuid

    # email should just be: username@astro.rug.nl, no need to store it ?
    # storing email anyway in case user wants to use a different email address

    def has_access(self, required_access_level):
        """Check if the user has the required access level."""
        return self.access_level >= required_access_level

    def __repr__(self):
        return f"User(\"{self.username}\")"


class Course(Base):
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(16), nullable=False, unique=True)
    semester = db.Column(db.String(16))
    description = db.Column(db.Text)

    # relation one-to-many: one course_level, many courses
    course_level_uuid = db.Column(GUID(),
                                  db.ForeignKey('course_level.uuid'),
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
    # 0 = not reviewed, 1 = approved, 2 = rejected
    approved = db.Column(db.Integer, default=0)
    sources = db.Column(db.Text)

    # relation one-to-many: one course, many questions
    course_uuid = db.Column(GUID(),
                            db.ForeignKey('course.uuid'),
                            nullable=False)
    course = db.relationship('Course',
                             backref=db.backref('questions', lazy=True))

    # relation one-to-many: one user, many questions
    user_uuid = db.Column(GUID(), db.ForeignKey(
        'user.uuid'), nullable=False)
    user = db.relationship('User', backref=db.backref('questions', lazy=True))

    # the many-to-many relations requires an extra table:
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships
    # TODO relation many-to-many: many: subject_tag, many: questions
    # TODO relation many-to-many: many: type_tag, many: questions

    subject_tags = db.relationship('SubjectTag', secondary=subject_tags,
                                   backref=db.backref('questions', lazy=True))

    def __repr__(self):
        return f"Question(\"{self.title}\")"


class SubjectTag(Base):
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"SubjectTag(\"{self.name}\")"


class Comment(Base):
    content = db.Column(db.Text, nullable=False)
    is_suggestion = db.Column(db.Boolean, nullable=False, default=False)

    # relation one-to-many: one: user, many: comments
    user_uuid = db.Column(GUID(), db.ForeignKey(
        'user.uuid'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    # relation one-to-many: one: question, many: comments
    question_uuid = db.Column(GUID(),
                              db.ForeignKey('question.uuid'),
                              nullable=False)
    question = db.relationship('Question',
                               backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"Comment(\"{self.content}\")"


class Answer(Base):
    content = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, nullable=False, default=False)
    sources = db.Column(MutableList.as_mutable(PickleType), default=[])

    # relation one-to-many: one: user, many: answers
    user_uuid = db.Column(GUID(), db.ForeignKey(
        'user.uuid'), nullable=False)
    user = db.relationship('User', backref=db.backref('answers', lazy=True))

    # relation one-to-many: one: question, many: answers
    question_uuid = db.Column(GUID(),
                              db.ForeignKey('question.uuid'),
                              nullable=False)
    question = db.relationship('Question',
                               backref=db.backref('answers', lazy=True))

    def __repr__(self):
        return f"Answer(\"{self.content}\")"


def init_db():
    db.create_all()
