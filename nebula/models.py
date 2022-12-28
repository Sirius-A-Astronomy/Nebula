import uuid

from passlib.hash import sha256_crypt
from sqlalchemy import DateTime, ForeignKey, PickleType, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import CHAR, TypeDecorator

from nebula import db


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
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
    uuid = db.Column(GUID(), primary_key=False, default=lambda: str(uuid.uuid4()))

    # Database uses utc time
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())


subject_tags = db.Table(
    "subject_tags",
    db.Column("subject_tag_uuid", GUID(), db.ForeignKey("subject_tag.uuid")),
    db.Column("question_uuid", GUID(), db.ForeignKey("question.uuid")),
)


subscriptions = db.Table(
    "subscriptions",
    db.Column("user_uuid", GUID(), db.ForeignKey("user.uuid")),
    db.Column("subscription_uuid", GUID(), db.ForeignKey("subscription.uuid")),
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

    # access_levels are defined in nebula/utilities.py

    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    username = db.Column(db.String(128), nullable=False, unique=True)
    access_level = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(128), nullable=True)

    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)

    subscriptions = db.relationship(
        "Subscription", secondary=subscriptions, backref=db.backref("users", lazy=True)
    )

    def get_id(self):
        return self.uuid

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        self.password = sha256_crypt.encrypt(password)
        db.session.commit()

    # email should just be: username@astro.rug.nl, no need to store it ?
    # storing email anyway in case user wants to use a different email address

    def has_access(self, required_access_level):
        """Check if the user has the required access level."""
        return self.access_level >= required_access_level

    def __repr__(self):
        return f'User("{self.username}")'


class Course(Base):
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(16), nullable=False, unique=True)
    semester = db.Column(db.String(16))
    description = db.Column(db.Text)

    # relation one-to-many: one course_level, many courses
    course_level_uuid = db.Column(
        GUID(), db.ForeignKey("course_level.uuid"), nullable=False
    )
    course_level = db.relationship(
        "CourseLevel", backref=db.backref("courses", lazy=True)
    )

    def __repr__(self):
        return f'Course("{self.name}")'


class CourseLevel(Base):
    # maybe we need a better name for the CourseLevel.name, as it
    #  referres to the year in which the course if given.
    name = db.Column(db.String(128), nullable=False)
    # maybe there is some kind of enumerate option for this:
    study_type = db.Column(db.String(64), nullable=False)
    code = db.Column(db.String(16), nullable=False, unique=True)

    def __repr__(self):
        return f'CourseLevel("{self.study_type}", "{self.name}")'


class Question(Base):
    title = db.Column(db.String(256), nullable=False)
    difficulty = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    # 0 = not reviewed, 1 = approved, 2 = rejected
    reviewed = db.Column(db.Integer, default=0)
    reviewed_by_uuid = db.Column(GUID(), db.ForeignKey("user.uuid"), nullable=True)
    reviewed_by = db.relationship("User", foreign_keys=[reviewed_by_uuid])

    sources = db.Column(db.Text)
    # relation one-to-many: one course, many questions
    course_uuid = db.Column(GUID(), db.ForeignKey("course.uuid"), nullable=False)
    course = db.relationship("Course", backref=db.backref("questions", lazy=True))

    # relation one-to-many: one user, many questions
    user_uuid = db.Column(GUID(), db.ForeignKey("user.uuid"), nullable=False)
    user = db.relationship(
        "User", foreign_keys=[user_uuid], backref=db.backref("questions", lazy=True)
    )

    # the many-to-many relations requires an extra table:
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships
    # TODO relation many-to-many: many: subject_tag, many: questions
    # TODO relation many-to-many: many: type_tag, many: questions

    subject_tags = db.relationship(
        "SubjectTag", secondary=subject_tags, backref=db.backref("questions", lazy=True)
    )

    def __repr__(self):
        return f'Question("{self.title}")'


class SubjectTag(Base):
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'SubjectTag("{self.name}")'


class Comment(Base):
    content = db.Column(db.Text, nullable=False)
    is_suggestion = db.Column(db.Boolean, nullable=False, default=False)

    # relation one-to-many: one: user, many: comments
    user_uuid = db.Column(GUID(), db.ForeignKey("user.uuid"), nullable=False)
    user = db.relationship("User", backref=db.backref("comments", lazy=True))

    # relation one-to-many: one: question, many: comments
    question_uuid = db.Column(GUID(), db.ForeignKey("question.uuid"), nullable=False)
    question = db.relationship("Question", backref=db.backref("comments", lazy=True))

    def __repr__(self):
        return f'Comment("{self.content}")'


class Answer(Base):
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, nullable=False, default=False)
    sources = db.Column(MutableList.as_mutable(PickleType), default=[])

    # relation one-to-many: one: user, many: answers
    user_uuid = db.Column(GUID(), db.ForeignKey("user.uuid"), nullable=False)
    user = db.relationship("User", backref=db.backref("answers", lazy=True))

    # relation one-to-many: one: question, many: answers
    question_uuid = db.Column(GUID(), db.ForeignKey("question.uuid"), nullable=False)
    question = db.relationship("Question", backref=db.backref("answers", lazy=True))

    def __repr__(self):
        return f'Answer("{self.content}")'


class Notification(Base):
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    link = db.Column(db.String(256))
    link_text = db.Column(db.String(256))
    category = db.Column(db.String(64), nullable=False, default="info")

    # relation one-to-many: one: user, many: notifications
    user_uuid = db.Column(GUID(), db.ForeignKey("user.uuid"), nullable=False)
    user = db.relationship("User", backref=db.backref("notifications", lazy=True))

    def __repr__(self):
        return f'Notification("{self.content}", {self.category})'


class Subscription(Base):
    # relation many-to-many: many: users, many: subscriptions

    # relation one-to-one: one: subscription, one: question
    question_uuid = db.Column(GUID(), db.ForeignKey("question.uuid"), nullable=False)
    question = db.relationship(
        "Question", backref=db.backref("subscriptions", lazy=True)
    )


def init_db():
    db.create_all()
