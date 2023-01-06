from nebula.models import Base, db


class SubjectTag(Base):
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'SubjectTag("{self.name}")'

    def expose(self):
        return {
            "id": self.uuid,
            "name": self.name,
        }
