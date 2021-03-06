from fiistudentrest.models import ScheduleClass, Student
from fiistudentrest.models import Course, Professor, Classroom
from fiistudentrest.api_functions.auth import verify_token
from fiistudentrest.utils import export_csv

import hug
import json


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


@hug.local()
@hug.get()
@hug.cli()
def schedule(request):
    """Gets the schedule for a logged user"""
    authorization = request.get_header('Authorization')
    if not authorization:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'No Authorization field exists in request header'}]}

    student_key_urlsafe = verify_token(authorization)
    if not student_key_urlsafe:
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
        professor_key = ent.professor
        classroom_key = ent.classroom

        if course_key is not None and professor_key is not None and classroom_key is not None:
            course = Course.get(course_key)    
            dictionary["name"] = course.title
            
            professor = Professor.get(professor_key)
            dictionary["professor"] = professor.firstName + ' ' + professor.lastName
            
            classroom = Classroom.get(classroom_key)
            dictionary['classroom'] = classroom.identifier

            dictionary["id"] = ent.urlsafe
            dictionary["course_id"] = course.urlsafe
            dictionary["type"] = ent.classType
            dictionary["abv"] = get_abbreviation(course.title)
            dictionary["startTime"] = str(ent.startHour)
            dictionary["endTime"] = str(ent.endHour)
            dictionary["day"] = str(ent.dayOfTheWeek)

            schedule_list.append(dictionary)

    json_data = json.dumps(schedule_list)
    return json_data


@hug.get()
def export(request):
    """Returns the data to be exported as csv"""
    authorization = request.get_header('Authorization')
    if not authorization:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'No Authorization field exists in request header'}]}

    student_key_urlsafe = verify_token(authorization)
    if not student_key_urlsafe:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'Header contains token, but it is not a valid one.'}]}


    student = Student.get(student_key_urlsafe)
    
    year_and_group = student.group
    csv_content = export_csv(year_and_group)

    return {'status':'ok', 'data':csv_content}   
