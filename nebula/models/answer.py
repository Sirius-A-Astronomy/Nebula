from sqlalchemy import PickleType
from sqlalchemy.ext.mutable import MutableList

from nebula.models import GUID, Base, db


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
