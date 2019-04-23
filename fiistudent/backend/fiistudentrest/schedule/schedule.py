import hug
import json

from fiistudentrest.models import ScheduleClass, Student
from fiistudentrest.models import Course


def get_abbreviation(title):
    """Gets the abreviation for the course"""
    # Can be improved
    raw_title = title.replace(" pentru ", " ")
    raw_title = raw_title.replace(" si ", " ")
    raw_title = raw_title.replace(" pe ", " ")
    raw_title = raw_title.replace(" de ", " ")
    raw_title = raw_title.replace(" din ", " ")
    raw_title = raw_title.replace(" in ", " ")
    raw_title = raw_title.replace(" ale ", " ")
    raw_title = raw_title.replace(":", " ")
    raw_title = raw_title.replace(",", " ")
    raw_title = raw_title.replace("-", " ")
    raw_title = raw_title.replace(" III", " ")
    raw_title = raw_title.replace(" II", " ")
    raw_title = raw_title.replace(" I", " ")

    raw_title = raw_title[0:47]
    raw_title_words = raw_title.split()

    abbreviation = ""
    for word in raw_title_words:
        abbreviation += word.upper()[0]
    return abbreviation


# def verifyCourseKey(course_key):
#     course_query = Course.query()
#     course_query_it = course_query.fetch()
#     for course_ent in course_query_it:
#         if course_ent.key == course_key:
#             return True
#     return False

@hug.local()
@hug.get()
@hug.cli()
def schedule(request):
    """ Gets the schedule for a logged user """
    authorization = request.get_header('Authorization')
    if not authorization:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'No Authorization field exists in request header'}]}

    student_key_urlsafe = verify_token(authorization)
    if not user_urlsafe:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'Header contains token, but it is not a valid one.'}]}


    student = Student.get(student_key_urlsafe)
    year_and_group = student.group

    schedule_query = ScheduleClass.query()
    schedule_query.add_filter('group', '=', year_and_group)
    schedule_query_it = schedule_query.fetch()

    schedule_list = []

    for ent in schedule_query_it:
        dictionary = {}
        course_key = ent.course

        if course_key is not None:
            course = Course.get(course_key)
            dictionary["id"] = ent.urlsafe
            dictionary["name"] = course.title
            dictionary["abv"] = get_abbreviation(course.title)
            dictionary["startTime"] = str(ent.startHour)
            dictionary["endTime"] = str(ent.endHour)
            dictionary["day"] = str(ent.dayOfTheWeek)

            schedule_list.append(dictionary)

    json_data = json.dumps(schedule_list)
    return json_data
