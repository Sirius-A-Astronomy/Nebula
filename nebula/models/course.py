from nebula.models import GUID, Base, db


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
