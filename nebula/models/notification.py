from nebula.models import GUID, Base, db


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
