from nebula.models import GUID, Base, db


class Course(Base):
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(16), nullable=False, unique=True)
    semester = db.Column(db.String(16))
    description = db.Column(db.Text)

    # relation one-to-many: one course_level, many courses
    course_level_uuid = db.Column(
        GUID(), db.ForeignKey("course_level.uuid"), nullable=True
    )
    course_level = db.relationship(
        "CourseLevel",
        backref=db.backref("courses", lazy=True, cascade="all, delete-orphan"),
    )

    def __repr__(self):
        return f'Course("{self.name}")'

    def expose(self):
        return {
            "id": self.uuid,
            "name": self.name,
            "code": self.code,
            "course_level": self.course_level.expose(),
            "description": self.description,
            "semester": self.semester,
        }
