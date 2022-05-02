import datetime
from nebula.models import CourseLevel, Course, Question, User, Comment

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
    User(username="johndoe", first_name="John", last_name="Doe"),
    User(username="sipma", first_name="Sten", last_name="Sipma"),
    User(username="nameless"),
]

questions = [
    Question(title="How to solve an equation",
             content="Solve for x: 2x + 1 = 0",
             answer="""First subtract one on both sides: 2x = -1,
             then divide by 2 to get the answer: x = -1/2""",
             user=users[0],
             course=courses[1]),
    Question(title="Is it possible to create a question with a date",
             content="I guess we see what happens",
             answer="""If implemented correctly, it is possible to specify
             an arbitrary creation date, by passing it as an argument to the
             question.""",
             created_at=datetime.date(1970, 1, 1),
             user=users[1],
             course=courses[0])
]

comments = [
    Comment(content="""This is an awefull question, as it is not related to
    Linear Algebra at all!""",
            user=users[2],
            question=questions[1])
]
