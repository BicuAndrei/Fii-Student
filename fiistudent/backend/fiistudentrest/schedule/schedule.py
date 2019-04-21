import hug

from fiistudentrest.models import ScheduleClass
from fiistudentrest.models import Course


def verify_year(year):
    """ Verify if the year is valid """
    if (year == 'I1' or year == 'I2' or year == 'I3') or (year == 'MOC' or year == 'MIS'):
        return True
    else:
        print('This is not a valid year')
        return False


def verify_group(group):
    """ Implement later if needed """
    return True


def get_abreviation(title):
    """Gets the abreviation for the course"""
    # Can be improved
    raw_title = title.replace(" pentru ", " ")
    raw_title = raw_title.replace(" si ", " ")
    raw_title = raw_title.replace(" pe ", " ")
    raw_title = raw_title.replace(" de ", " ")
    raw_title = raw_title.replace(" din ", " ")
    raw_title = raw_title.replace(" ale ", " ")
    raw_title = raw_title.replace(":", " ")
    raw_title = raw_title.replace("-", " ")
    raw_title = raw_title.replace(" III", " ")
    raw_title = raw_title.replace(" II", " ")
    raw_title = raw_title.replace(" I", " ")

    raw_title = raw_title[0:47]
    raw_title_words = raw_title.split()

    abreviation = ""
    for word in raw_title_words:
        abreviation += word.upper()[0]
    return abreviation


@hug.local()
@hug.get()
@hug.cli()
def get_schedule(year: hug.types.text, group: hug.types.text):
    """ Gets the schedule for a logged user """
    year_and_group = str(year) + str(group)
    first_it = '{'
    response = ""

    if verify_year(year) and verify_group(group):
        schedule_query = ScheduleClass.query()
        schedule_query.add_filter('group', '=', year_and_group)
        schedule_query_it = schedule_query.fetch()

        response = '['
        for ent in schedule_query_it:
            response += first_it
            first_it = ', {'
            course_key = ent.course
            response += '"id": "' + ent.urlsafe
            if course_key is not None:
                course = Course.get(course_key)
                response += '", "name": "' + course.title
                response += '", "abv": "' + get_abreviation(course.title)
            else:
                response += '", "name": "' + str(course_key)
                response += '", "abv": "' + str(course_key)
            response += '", "startTime": "' + str(ent.startHour)
            response += '", "endTime": "' + str(ent.endHour)
            response += '", "day": "' + str(ent.dayOfTheWeek)
            response += '"}'
        response += ']'
    return response
