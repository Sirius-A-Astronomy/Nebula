from nebula.models import GUID, Base, db


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
