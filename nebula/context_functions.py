import datetime


def context_processor():
    # This function is called by the flask template engine and returns a dictionary of variables and functions
    def get_current_year():
        return datetime.datetime.now().year

    from nebula.models import CourseLevel, Course
    nav = {
        "CourseLevels":
            {   "Bachelor": CourseLevel.query.filter_by(study_type='Bachelor').all(),
                "Master": CourseLevel.query.filter_by(study_type='Master').all()
            },
        "Courses":
            {   "bsc-yr1": Course.query.filter_by(course_level_id=1).all(),
                "bsc-yr2": Course.query.filter_by(course_level_id=2).all(),
                "bsc-yr3": Course.query.filter_by(course_level_id=3).all(),
                "msc": Course.query.filter_by(course_level_id=4).all()
            }
        
        }

    return dict(current_year = get_current_year(), nav = nav)
