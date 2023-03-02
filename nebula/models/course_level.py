from nebula.models import Base, db


class CourseLevel(Base):
    # maybe we need a better name for the CourseLevel.name, as it
    #  referres to the year in which the course if given.
    name = db.Column(db.String(128), nullable=False)
    # maybe there is some kind of enumerate option for this:
    study_type = db.Column(db.String(64), nullable=False)
    code = db.Column(db.String(16), nullable=False, unique=True)

    def __repr__(self):
        return f'CourseLevel("{self.study_type}", "{self.name}")'

    def expose(self):
        return {
            "id": self.uuid,
            "name": self.name,
            "code": self.code,
            "study_type": self.study_type,
        }
