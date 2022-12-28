from nebula.models import GUID, Base, db


class Subscription(Base):
    # relation many-to-many: many: users, many: subscriptions

    # relation one-to-one: one: subscription, one: question
    question_uuid = db.Column(GUID(), db.ForeignKey("question.uuid"), nullable=False)
    question = db.relationship(
        "Question", backref=db.backref("subscriptions", lazy=True)
    )
