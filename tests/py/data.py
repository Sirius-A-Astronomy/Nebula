import datetime

from passlib.hash import sha256_crypt

from nebula.models.comment import Comment
from nebula.models.course import Course
from nebula.models.course_level import CourseLevel
from nebula.models.question import Question
from nebula.models.user import User

course_levels = [
    CourseLevel(name="First Year", study_type="Bachelor", code="bsc-yr1"),
    CourseLevel(name="Second Year", study_type="Bachelor", code="bsc-yr2"),
    CourseLevel(name="Third Year", study_type="Bachelor", code="bsc-yr3"),
    CourseLevel(name="General", study_type="Master", code="msc"),
]

courses = [
    Course(name="Linear Algebra", code="WILA1-06"),
    Course(name="Calculus 1", code="WICAL1-12"),
    Course(name="Thermal Physics", code="WBPH19001"),
    Course(name="Numerical Methods", code="WBAS17001"),
    Course(name="Interstellar Medium", code="STISME5"),
    Course(name="Astrophysical Hydrodynamics", code="STAF3E5"),
    Course(name="General Relativity", code="NAGR-08"),
    Course(name="Student Seminar Quantum Universe", code="NASSC-09"),
]

course_levels[0].courses.extend(courses[0:2])
course_levels[1].courses.extend(courses[2:4])
course_levels[2].courses.extend(courses[4:6])
course_levels[3].courses.extend(courses[6:8])

users = [
    User(email="john@example.com", first_name="John", last_name="Doe"),
    User(email="sipma@kapteyn.nl", first_name="Sten", last_name="Sipma"),
    User(email="nameless@mail.com"),
]

for user in users:
    hashed_password = sha256_crypt.hash("password")
    user.password = hashed_password

questions = [
    Question(
        title="How to solve an equation",
        content="Solve for x: 2x + 1 = 0",
        user=users[0],
        course=courses[1],
    ),
    Question(
        title="Is it possible to create a question with a date",
        content="I guess we see what happens",
        created_at=datetime.date(1970, 1, 1),
        user=users[1],
        course=courses[0],
    ),
]

comments = [
    Comment(
        content="""This is an awefull question, as it is not related to
    Linear Algebra at all!""",
        user=users[2],
        question=questions[1],
    )
]
