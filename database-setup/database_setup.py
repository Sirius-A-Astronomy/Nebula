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

    # General Master
    Course(name="General Relativity",
        code="WMPH009-05",
        description="",
        course_level=course_levels[3],
        semester="1a"),
    Course(name="Electrodynamics of Radiation Processes",
        code="WMAS008-05",
        description="",
        course_level=course_levels[3],
        semester="1a"),
]

db.session.add_all(course_levels)
db.session.commit()

users = [
    User(username="johndoe", firstname="John", lastname="Doe"),
    User(username="sipma", firstname="Sten", lastname="Sipma"),
    User(username="nameless"),
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
                course=Course.query.filter_by(name = "Linear Algebra (for Physics)").first(),
                difficulty = "Hard"),
    Question(title="Is it possible to create a question with a date",
             content="I guess we see what happens",
             answer="""If implemented correctly, it is possible to specify
             an arbitrary creation date, by passing it as an argument to the
             question.""",
             creation_datetime=datetime.date(2021, 9, 2),
             user=users[1],
             course=courses[0])
]

comments = [
    Comment(content="""This is an awful question, as it is not related to
    Linear Algebra at all!""",
            user=users[2],
            question=questions[1])
]
db.session.add_all(questions)
db.session.commit()