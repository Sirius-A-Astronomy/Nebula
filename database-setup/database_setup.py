from nebula import db, create_app
import datetime
from nebula.models import User, Course, CourseLevel, Question, Comment

app = create_app()

app.app_context().push()

for column in [User, Course, CourseLevel, Question, Comment]:
    column.query.delete()
db.session.commit()


course_levels = [
    CourseLevel(name="First Year", study_type="Bachelor", code="bsc-yr1"),
    CourseLevel(name="Second Year", study_type="Bachelor", code="bsc-yr2"),
    CourseLevel(name="Third Year", study_type="Bachelor", code="bsc-yr3"),
    CourseLevel(name="General", study_type="Master", code="msc"),
]

courses = [
    # First Year Bachelor
    Course(name="Mechanics and Relativity",
           code="WBPH001-10",
           description="This course addresses topics in special relativity and mechanics at varying levels of mathematical complexity.",
           course_level=course_levels[0],
           semester="1"),
    Course(name="Calculus 1",
           code="WBMA003-05",
           description="This course introduces the basic concepts of quantum mechanics and its application to the study of the universe.",
           course_level=course_levels[0],
           semester="1a"),
    Course(name="Physics Laboratory 1",
           code="WBPH013-05",
           description="",
           course_level=course_levels[0],
           semester="1a"),
    Course(name="Linear Algebra (for Physics)",
           code="WBPH054-05",
           description="Linear algebra is the branch of mathematics concerning linear equations.",
           course_level=course_levels[0],
           semester="1b"),
    Course(name="Introduction Astronomy",
           code="WBAS007-05",
           description="Magnitudes, methods to measure distances, black bodies, spectra of stars, Hertzsprung-Russell diagram, binary stars, methods to measure stellar masses, stellar structure and evolution, the interstellar medium, star formation, the Milky Way and other galaxies, large scale structure, cosmology/Big Bang, the Solar System",
           course_level=course_levels[0],
           semester="1b"),
    Course(name="Electricity and Magnetism",
           code="WBPH033-10",
           description="",
           course_level=course_levels[0],
           semester="2"),
    Course(name="Calculus 2",
           code="WBMA029-05",
           description="",
           course_level=course_levels[0],
           semester="2a"),
    Course(name="Introduction to Programming and Computational Methods",
           code="WBAS013-05",
           description="",
           course_level=course_levels[0],
           semester="2a"),
    Course(name="Mathematical Physics",
           code="WBPH049-05",
           description="",
           course_level=course_levels[0],
           semester="2b"),
    Course(name="Observational Astronomy",
           code="WBAS015-05",
           description="",
           course_level=course_levels[0],
           semester="2b"),


    # Second Year Bachelor
    Course(name="Thermal Physics",
           code="WBPH002-10",
           description="",
           course_level=course_levels[1],
           semester="1"),
    Course(name="Quantum Physics 1",
           code="WBPH014-05",
           description="",
           course_level=course_levels[1],
           semester="1a"),
    Course(name="Statistics for Astronomy",
           code="WBAS004-05",
           description="The objective of the course is to get an introduction into commonly used statistical methods in astronomy and to familiarize students with measurement errors. The course is focussed on the Bayesian approach to statistics, and starts with basic probability theory. The student is introduced to the estimation of single and multiple parameters from data. Several probability distribution functions are presented and their use is explained. The concepts of maximum likelihood, hypothesis testing, model selection and model fitting are covered, with emphasis on fitting data to a straight line.",
           course_level=course_levels[1],
           semester="1a"),
    Course(name="Complex Analysis",
           code="WBMA018-05",
           description="",
           course_level=course_levels[1],
           semester="1b"),
    Course(name="Waves and Optics",
           code="WBPH032-05",
           description="",
           course_level=course_levels[1],
           semester="1b"),
    Course(name="Numerical Methods",
           code="WBAS014-05",
           description="",
           course_level=course_levels[1],
           semester="2a"),
    Course(name="Physics, Astronomy & Society: Ethical & Professional Aspects",
           code="WBPH053-05",
           description="",
           course_level=course_levels[1],
           semester="2a"),
    Course(name="Structure of Matter 1",
           code="WBPH046-05",
           description="",
           course_level=course_levels[1],
           semester="2a"),
    Course(name="Physics of Galaxies",
           code="WBAS016-05",
           description="",
           course_level=course_levels[1],
           semester="2b"),
    Course(name="Physics of Stars",
           code="WBAS017-05",
           description="",
           course_level=course_levels[1],
           semester="2b"),
    Course(name="Quantum Physics 2",
           code="WBPH052-05",
           description="",
           course_level=course_levels[1],
           semester="2b"),

    # Third Year Bachelor
    Course(name="Astroparticle Physics",
           code="WBPH036-05",
           description="",
           course_level=course_levels[2],
           semester="2a"),
    Course(name="Astrophysical Hydrodynamics",
           code="WBAS011-05",
           description="",
           course_level=course_levels[2],
           semester="2a"),
    Course(name="Interstellae medium",
           code="WBAS012-05",
           description="",
           course_level=course_levels[2],
           semester="2a"),
    Course(name="Astronomy Bachelor Research Project",
           code="WBAS901-15",
           description="",
           course_level=course_levels[2],
           semester="2b"),

    # General Master
    Course(name="General Relativity",
           code="WMPH009-05",
           description="",
           course_level=course_levels[3],
           semester="1a"),
    Course(name="Introduction to Data Science",
           code="WMCS002-05",
           description="",
           course_level=course_levels[3],
           semester="1a"),
    Course(name="Electrodynamics of Radiation Processes",
           code="WMAS008-05",
           description="",
           course_level=course_levels[3],
           semester="1b"),
    Course(name="Particle Phyics Phenomenology",
           code="WMPH026-05",
           description="",
           course_level=course_levels[3],
           semester="2a"),
    Course(name="Student Seminar Quantum Universe",
           code="WMPH039-05",
           description="",
           course_level=course_levels[3],
           semester="2b")
]

db.session.add_all(course_levels)
db.session.commit()

users = [
    User(username="johndoe", firstname="John", lastname="Doe"),
    User(username="sipma", firstname="Sten", lastname="Sipma"),
    User(username="hans", firstname="Hans", lastname="Wurst"),
    User(username="james", firstname="James", lastname="Bond"),
    User(username="matt", firstname="Matt", lastname="Harrison"),
    User(username="nathan", firstname="Nathan", lastname="Baker"),
    User(username="jeff", firstname="Jeff", lastname="Baker"),
    User(username="joseph", firstname="Joseph", lastname="Baker"),
    User(username="julian", firstname="Julian", lastname="Baker")
]

questions = [
    Question(title="How to solve an equation",
             content="Solve for x: 2x + 1 = 0",
             answer="""First subtract one on both sides: 2x = -1,
             then divide by 2 to get the answer: x = -1/2""",
             user=users[0],
             course=Course.query.filter_by(code="WBPH054-05").first()),
    Question(title="This is another question",
             content="It has different content",
             answer="This is the answer",
             user=users[1],
             course=Course.query.filter_by(
                 name="Linear Algebra (for Physics)").first(),
             difficulty="Hard"),
    Question(title="Is it possible to create a question with a date",
             content="I guess we see what happens",
             answer="""If implemented correctly, it is possible to specify
             an arbitrary creation date, by passing it as an argument to the
             question.""",
             creation_datetime=datetime.date(2021, 9, 2),
             user=users[1],
             course=courses[0]),
    Question(title="What is the answer to this question?",
             content="I don't know",
             answer="42",
             user=users[2],
             course=Course.query.filter_by(name="General Relativity").first()),
    Question(title="How to solve a system of equations",
             content="Solve for x and y: 2x + y = 1, 3x + y = 2",
             answer="""First subtract one on both sides: 2x + y = -1, 3x + y = -2,
                then divide by 2 to get the answer: x = -1/2, y = -3/2""",
             user=users[3],
             course=Course.query.filter_by(name="Linear Algebra (for Physics)").first()),
    Question(title="How to take the derivative of a function",
             content="Take the derivative of f(x) = x^2",
             answer="""The derivative of f(x) is 2x""",
             user=users[4],
             course=Course.query.filter_by(name="Calculus 1").first()),
    Question(title="How to solve a differential equation",
             content="Solve for x: x'' = -x",
             answer="""The solution is x = 0""",
             user=users[2],
             course=Course.query.filter_by(name="Calculus 1").first()),
    Question(title="How to find the determinant of a matrix",
             content="Find the determinant of the matrix {{ 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 }}",
             answer="""The determinant is:
                1*(5*6 - 9*4) - 2*(3*6 - 8*4) + 3*(3*4 - 8*2) =
                -2*(3*6 - 8*4) + 3*(3*4 - 8*2) =
                -1*(3*6 - 8*4) + 3*(3*4 - 8*2) =
                -(3*6 - 8*4) + 3*(3*4 - 8*2) =
                -6 + 6 =
                2""",
             user=users[5],
             course=Course.query.filter_by(name="Linear Algebra (for Physics)").first()),
    Question(title="How to invert a matrix",
             content="Invert the matrix {{ 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 }}",
             answer="""The inverse is:
                {{ -3,  2,  1 }, {  2, -1, -1 }, { -1,  1,  0 }}
                """,
             user=users[4],
             course=Course.query.filter_by(name="Linear Algebra (for Physics)").first()),
    Question(title="How to find the eigenvalues of a matrix",
             content="Find the eigenvalues of the matrix {{ 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 }}",
             answer="""The eigenvalues are:
                1, 2, 3
                4, 5, 6
                7, 8, 9
                """,
             user=users[6],
             course=Course.query.filter_by(name="Linear Algebra (for Physics)").first()),
    Question(title="How to find the eigenvectors of a matrix",
             content="Find the eigenvectors of the matrix {{ 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 }}",
             answer="""The eigenvectors are:
                1, 0, 0
                0, 1, 0
                0, 0, 1
                """,
             user=users[5],
             course=Course.query.filter_by(name="Linear Algebra (for Physics)").first()),
    Question(title="How to find the characteristic polynomial of a matrix",
             content="Find the characteristic polynomial of the matrix {{ 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 }}",
             answer="""The characteristic polynomial is:
                x^3 + 2*x^2 + 3*x + 1
                """,
             user=users[7],
             course=Course.query.filter_by(name="Linear Algebra (for Physics)").first())

]

comments = [
    Comment(content="""This is an awful question, as it is not related to
    Linear Algebra at all!""",
            user=users[2],
            question=questions[1])
]
db.session.add_all(questions)
db.session.commit()
