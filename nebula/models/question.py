from nebula.models import GUID, Base, db

subject_tags = db.Table(
    "subject_tags",
    db.Column("subject_tag_uuid", GUID(), db.ForeignKey("subject_tag.uuid")),
    db.Column("question_uuid", GUID(), db.ForeignKey("question.uuid")),
)


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
    course_uuid = db.Column(GUID(), db.ForeignKey("course.uuid"), nullable=True)
    course = db.relationship("Course", backref=db.backref("questions", lazy=True, cascade="all, delete-orphan"))

    # relation one-to-many: one user, many questions
    user_uuid = db.Column(GUID(), db.ForeignKey("user.uuid"), nullable=False)
    user = db.relationship(
        "User", foreign_keys=[user_uuid], backref=db.backref("questions", lazy=True, cascade="all, delete-orphan")
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

    def expose(self):
        return {
            "id": self.uuid,
            "title": self.title,
            "content": self.content,
            "course": self.course.expose(),
            "user": self.user.expose(),
            "subject_tags": [subject_tag.expose() for subject_tag in self.subject_tags],
            "answers": [answer.expose() for answer in self.answers],
            "comments": [comment.expose() for comment in self.comments],
        }
