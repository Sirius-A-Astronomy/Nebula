from flask import Blueprint
from flask.cli import with_appcontext
from nebula import db, create_app
from sqlalchemy.exc import IntegrityError
import json
from nebula.models import Course, CourseLevel


bp = Blueprint('cli_db', __name__, cli_group="db")


@bp.cli.command('init')
@with_appcontext
def cli_init_db():
    db.create_all()


@bp.cli.command('drop')
@with_appcontext
def cli_drop_db():
    if (input("Are you sure you want to drop all database tables? (y/[n]): ") != "y"):
        print("Drop cancelled")
        return
    db.drop_all()


@bp.cli.command('reset')
@with_appcontext
def cli_reset_db():
    if (input("Are you sure you want to reset the database? (y/[n]): ") != "y"):
        print("Reset cancelled")
        return
    db.drop_all()
    db.create_all()


@bp.cli.command('seed')
@with_appcontext
def cli_seed_db():

    json_file = open("seed_data/courses.json", "r")
    courses_json = json.load(json_file)
    json_file.close()

    for course_level in courses_json["course_levels"]:
        new_course_level = CourseLevel(
            name=course_level["name"],
            study_type=course_level["study_type"],
            code=course_level["code"],
        )

        db.session.add(new_course_level)

        for course in course_level["courses"]:
            course = Course(
                name=course["name"],
                code=course["code"],
                description=course["description"],
                course_level=new_course_level,
                semester=course["semester"],
            )

            db.session.add(course)

    try:
        db.session.commit()
    except IntegrityError as e:
        print("Error while seeding database", e)


# Reference for if we can still use some of the old data in the new JSON file
course_levels = [
    CourseLevel(name="First Year", study_type="Bachelor", code="bsc-yr1"),
    CourseLevel(name="Second Year", study_type="Bachelor", code="bsc-yr2"),
    CourseLevel(name="Third Year", study_type="Bachelor", code="bsc-yr3"),
    CourseLevel(name="General", study_type="Master", code="msc"),
]

courses = [
    # First Year Bachelor
    Course(
        name="Mechanics and Relativity",
        code="WBPH001-10",
        description="This course addresses topics in special relativity and mechanics at varying levels of mathematical complexity.",
        course_level=course_levels[0],
        semester="1",
    ),
    Course(
        name="Calculus 1",
        code="WBMA003-05",
        description="This course introduces the basic concepts of quantum mechanics and its application to the study of the universe.",
        course_level=course_levels[0],
        semester="1a",
    ),
    Course(
        name="Physics Laboratory 1",
        code="WBPH013-05",
        description="",
        course_level=course_levels[0],
        semester="1a",
    ),
    Course(
        name="Linear Algebra (for Physics)",
        code="WBPH054-05",
        description="Linear algebra is the branch of mathematics concerning linear equations.",
        course_level=course_levels[0],
        semester="1b",
    ),
    Course(
        name="Introduction Astronomy",
        code="WBAS007-05",
        description="Magnitudes, methods to measure distances, black bodies, spectra of stars, Hertzsprung-Russell diagram, binary stars, methods to measure stellar masses, stellar structure and evolution, the interstellar medium, star formation, the Milky Way and other galaxies, large scale structure, cosmology/Big Bang, the Solar System",
        course_level=course_levels[0],
        semester="1b",
    ),
    Course(
        name="Electricity and Magnetism",
        code="WBPH033-10",
        description="",
        course_level=course_levels[0],
        semester="2",
    ),
    Course(
        name="Calculus 2",
        code="WBMA029-05",
        description="",
        course_level=course_levels[0],
        semester="2a",
    ),
    Course(
        name="Introduction to Programming and Computational Methods",
        code="WBAS013-05",
        description="",
        course_level=course_levels[0],
        semester="2a",
    ),
    Course(
        name="Mathematical Physics",
        code="WBPH049-05",
        description="",
        course_level=course_levels[0],
        semester="2b",
    ),
    Course(
        name="Observational Astronomy",
        code="WBAS015-05",
        description="",
        course_level=course_levels[0],
        semester="2b",
    ),
    # Second Year Bachelor
    Course(
        name="Thermal Physics",
        code="WBPH002-10",
        description="",
        course_level=course_levels[1],
        semester="1",
    ),
    Course(
        name="Quantum Physics 1",
        code="WBPH014-05",
        description="",
        course_level=course_levels[1],
        semester="1a",
    ),
    Course(
        name="Statistics for Astronomy",
        code="WBAS004-05",
        description="The objective of the course is to get an introduction into commonly used statistical methods in astronomy and to familiarize students with measurement errors. The course is focussed on the Bayesian approach to statistics, and starts with basic probability theory. The student is introduced to the estimation of single and multiple parameters from data. Several probability distribution functions are presented and their use is explained. The concepts of maximum likelihood, hypothesis testing, model selection and model fitting are covered, with emphasis on fitting data to a straight line.",
        course_level=course_levels[1],
        semester="1a",
    ),
    Course(
        name="Complex Analysis",
        code="WBMA018-05",
        description="",
        course_level=course_levels[1],
        semester="1b",
    ),
    Course(
        name="Waves and Optics",
        code="WBPH032-05",
        description="",
        course_level=course_levels[1],
        semester="1b",
    ),
    Course(
        name="Numerical Methods",
        code="WBAS014-05",
        description="",
        course_level=course_levels[1],
        semester="2a",
    ),
    Course(
        name="Physics, Astronomy & Society: Ethical & Professional Aspects",
        code="WBPH053-05",
        description="",
        course_level=course_levels[1],
        semester="2a",
    ),
    Course(
        name="Structure of Matter 1",
        code="WBPH046-05",
        description="",
        course_level=course_levels[1],
        semester="2a",
    ),
    Course(
        name="Physics of Galaxies",
        code="WBAS016-05",
        description="",
        course_level=course_levels[1],
        semester="2b",
    ),
    Course(
        name="Physics of Stars",
        code="WBAS017-05",
        description="",
        course_level=course_levels[1],
        semester="2b",
    ),
    Course(
        name="Quantum Physics 2",
        code="WBPH052-05",
        description="",
        course_level=course_levels[1],
        semester="2b",
    ),
    # Third Year Bachelor
    Course(
        name="Astroparticle Physics",
        code="WBPH036-05",
        description="",
        course_level=course_levels[2],
        semester="2a",
    ),
    Course(
        name="Astrophysical Hydrodynamics",
        code="WBAS011-05",
        description="",
        course_level=course_levels[2],
        semester="2a",
    ),
    Course(
        name="Interstellar medium",
        code="WBAS012-05",
        description="",
        course_level=course_levels[2],
        semester="2a",
    ),
    Course(
        name="Astronomy Bachelor Research Project",
        code="WBAS901-15",
        description="",
        course_level=course_levels[2],
        semester="2b",
    ),
    # General Master
    Course(
        name="General Relativity",
        code="WMPH009-05",
        description="",
        course_level=course_levels[3],
        semester="1a",
    ),
    Course(
        name="Introduction to Data Science",
        code="WMCS002-05",
        description="",
        course_level=course_levels[3],
        semester="1a",
    ),
    Course(
        name="Electrodynamics of Radiation Processes",
        code="WMAS008-05",
        description="",
        course_level=course_levels[3],
        semester="1b",
    ),
    Course(
        name="Particle Phyics Phenomenology",
        code="WMPH026-05",
        description="",
        course_level=course_levels[3],
        semester="2a",
    ),
    Course(
        name="Student Seminar Quantum Universe",
        code="WMPH039-05",
        description="",
        course_level=course_levels[3],
        semester="2b",
    ),
]
