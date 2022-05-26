from re import sub
from nebula import db, create_app
import datetime
from random import randrange
from datetime import timedelta
from nebula.models import User, Course, CourseLevel, Question, Comment, Answer, SubjectTag
from nebula.views.user import create_user

app = create_app()

app.app_context().push()

for column in [User, Course, CourseLevel, Question, Comment, Answer]:
    column.query.delete()
db.session.commit()


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


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
    Course(name="Interstellar medium",
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
    create_user("test_user", "unsafe", email="test_user1@nebula.com",
                access_level=1, first_name="Test", last_name="User1"),
    create_user("test_user2", "unsafe", email="test_user2@nebula.com",
                access_level=1, first_name="Test", last_name="User2"),
    create_user("test_moderator1", "unsafe", email="test_moderator1@nebula.com",
                access_level=2, first_name="Test", last_name="Moderator1"),
    create_user("test_moderator2", "unsafe", email="test_moderator2@nebula.com",
                access_level=2, first_name="Test", last_name="Moderator2"),
    create_user("test_admin", "unsafe", email="test_admin@nebula.com",
                access_level=3, first_name="Test", last_name="Admin"),

    create_user("pieterh", "unsafe", email="pieterh@nebula.com",
                access_level=3, first_name="Pieter", last_name="Huizenga"),
]

subject_tags = {
    "Astronomy":     SubjectTag(name="Astronomy"),
    "Astrophysics":  SubjectTag(name="Astrophysics"),
    "Computing":     SubjectTag(name="Computing"),
    "Earth Science": SubjectTag(name="Earth Science"),
    "Mathematics":   SubjectTag(name="Mathematics"),
    "Physics":       SubjectTag(name="Physics"),
    "Quantum Physics": SubjectTag(name="Quantum Physics"),
    "Statistics":    SubjectTag(name="Statistics")
}


print(users)
questions = [
    Question(title="What is the answer to life, the universe and everything?",
             content="How do you know?",
             course=courses[0],
             subject_tags=[subject_tags["Physics"]],
             user=users[5]),
    Question(title="This is the first question",
             content="This is the first content",
             course=courses[0],
             subject_tags=[subject_tags["Mathematics"]],
             user=users[5]),
    Question(title="This is the second question",
             content="This is the second content",
             course=courses[0],
             subject_tags=[subject_tags["Statistics"]],
             user=users[5]),
    Question(title="This is the third question",
             content="This is the third content",
             course=courses[13],
             subject_tags=[subject_tags["Astronomy"],
                           subject_tags["Astrophysics"], subject_tags["Computing"]],
             user=users[5]),
    Question(title="This is the fourth question",
             content="This is the fourth content",
             course=courses[0],
             subject_tags=[subject_tags["Earth Science"],
                           subject_tags["Mathematics"]],
             user=users[3]),
    Question(title="This is the fifth question",
             content="This is the fifth content",
             course=courses[0],
             subject_tags=[subject_tags["Physics"],
                           subject_tags["Quantum Physics"]],
             user=users[2]),
    Question(title="This is the sixth question",
             content="This is the sixth content",
             course=courses[0],
             subject_tags=[subject_tags["Physics"],
                           subject_tags["Quantum Physics"]],
             user=users[1]),
    Question(title="This is the seventh question",
             content="This is the seventh content",
             course=courses[0],
             subject_tags=[subject_tags["Statistics"],
                           subject_tags["Quantum Physics"]],
             user=users[0]),
    Question(title="This is the eighth question",
             content="This is the eighth content",
             course=courses[0],
             subject_tags=[subject_tags["Physics"]],
             user=users[0]),
    Question(title="This is the ninth question",
             content="This is the ninth content",
             course=courses[0],
             subject_tags=[subject_tags["Physics"]],
             user=users[4]),
    Question(title="This is the tenth question",
             content="This is the tenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[1]),
    Question(title="This is the eleventh question",
             content="This is the eleventh content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[0]),
    Question(title="This is the twelfth question",
             content="This is the twelfth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[4]),
    Question(title="This is the thirteenth question",
             content="This is the thirteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[0]),
    Question(title="This is the fourteenth question",
             content="This is the fourteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[3]),
    Question(title="This is the fifteenth question",
             content="This is the fifteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[2]),
    Question(title="This is the sixteenth question",
             content="This is the sixteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[4]),
    Question(title="This is the seventeenth question",
             content="This is the seventeenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[1]),
    Question(title="This is the eighteenth question",
             content="This is the eighteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[3]),
    Question(title="This is the nineteenth question",
             content="This is the nineteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[2]),
    Question(title="This is the twentieth question",
             content="This is the twentieth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[4]),
    Question(title="This is the twenty-first question",
             content="This is the twenty-first content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[0]),
]

Answers = [
    Answer(content="42",
           question=questions[0],
           sources=["https://www.google.com",
                    "https://www.wikipedia.org", "https://www.youtube.com"],
           user=users[5]),
    Answer(content="This is the first answer",
           question=questions[0],
           sources=["https://www.google.com",
                    "https://www.wikipedia.org", "https://rug.nl"],
           user=users[2]),
    Answer(content="This is the second answer",
           question=questions[0],
           sources=["https://www.google.com"],
           user=users[3]),
    Answer(content="This is the third answer",
           question=questions[1],
           sources=["https://www.google.com"],
           user=users[1]),
    Answer(content="This is the fourth answer",
           question=questions[2],
           sources=["https://www.google.com"],
           user=users[5]),
    Answer(content="This is the fifth answer",
           question=questions[3],
           sources=["https://www.google.com"],
           user=users[5]),
    Answer(content="This is the sixth answer",
           question=questions[3],
           sources=["https://www.google.com"],
           user=users[5]),
    Answer(content="This is the seventh answer",
           question=questions[3],
           sources=["https://www.google.com"],
           user=users[5]),
    Answer(content="This is the eighth answer",
           question=questions[3],
           user=users[5]),

]


comments = [
    Comment(content="This is the first comment",
            question=questions[0],
            user=users[5]),
    Comment(content="This is the second comment",
            question=questions[0],
            user=users[4]),
    Comment(content="This is the third comment",
            question=questions[0],
            user=users[2]),
    Comment(content="This is the fourth comment",
            question=questions[0],
            user=users[5])
]


db.session.add_all(users)


db.session.add_all(questions)

db.session.commit()
