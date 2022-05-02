from datetime import datetime, timezone


def context_processor():
    # This function is called by the flask template engine and returns a dictionary of variables and functions
    def get_current_year():
        """Returns the current year."""
        return datetime.now().year

    from nebula.models import CourseLevel, Course

    nav = {
        "CourseLevels":
            {"Bachelor": CourseLevel.query.filter_by(study_type='Bachelor').all(),
                "Master": CourseLevel.query.filter_by(study_type='Master').all()
             }

    }

    def utc_to_local(utc_dt):
        """Converts a UTC datetime object to a local datetime object."""
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def pretty_date(time=False):
        """
        Uses utc_to_local to convert the datetime object to local time
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc

        :param time: The datetime object or Epoch timestamp to convert.
        :type time: datetime or int
        """
        from datetime import datetime
        now = datetime.now().astimezone(tz=None)
        if type(time) is int:
            diff = now - datetime.fromtimestamp(utc_to_local(time))
        elif isinstance(time, datetime):
            diff = now - utc_to_local(time)
        elif not time:
            diff = 0
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return 'In the future?'

        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + " seconds ago"
            if second_diff < 120:
                return "a minute ago"
            if second_diff < 3600:
                return str(second_diff // 60) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str(second_diff // 3600) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + " days ago"
        if day_diff < 14:
            return "a week ago"
        if day_diff < 31:
            return str(day_diff // 7) + " weeks ago"
        if day_diff < 60:
            return "a month ago"
        if day_diff < 365:
            return str(day_diff // 30) + " months ago"
        if day_diff < (365 * 2):
            return "a year ago"
        if day_diff < (365 * 10):
            return str(day_diff // 365) + " years ago"
        if day_diff < (365 * 20):
            return "a decade ago"
        return str(day_diff // 3650) + " decades ago"

    return dict(
        current_year=get_current_year(),
        nav=nav,
        utc_to_local=utc_to_local,
        pretty_date=pretty_date)
