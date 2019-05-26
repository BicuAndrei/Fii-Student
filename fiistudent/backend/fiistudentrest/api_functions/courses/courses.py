import hug
import json
import datetime

from fiistudentrest.models.course import Course
from fiistudentrest.api_functions.auth import verify_token


def get_classes(day_of_the_week):
    """ Returneaza toate orele dintr-o anumita zi """
    days = ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri', 'Sambata', 'Duminica']
    query = ScheduleClass.query()
    query.add_filter('dayOfTheWeek', '=', days[day_of_the_week])
    query_it = query.fetch()
    return list(query_it)


@hug.local()
@hug.get()
@hug.cli()
def courses(request):
    """Retrieves all courses"""
    authorization = request.get_header('Authorization')
    if not authorization:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'No Authorization field exists in request header'}]}

    user_urlsafe = verify_token(authorization)
    if not user_urlsafe:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'Header contains token, but it is not a valid one.'}]}

    data_list = []
    data1 = {}
    data2 = {}
    data3 = {}
    data4 = {}
    data5 = {}

    subjects_list1 = []
    subjects_list2 = []
    subjects_list3 = []
    subjects_list4 = []
    subjects_list5 = []

    data1["year"] = 'I1'
    data2["year"] = 'I2'
    data3["year"] = 'I3'
    data4["year"] = 'M1'
    data5["year"] = 'M2'

    course_query = Course.query()
    course_query_it = course_query.fetch()

    for ent in course_query_it:
        subjects_dict = {}
        subjects_dict["id"] = ent.urlsafe
        subjects_dict["name"] = ent.title
        subjects_dict["link"] = ent.link
        subjects_dict["fisa"] = ent.sub_desc
        course_year = ent.year
        course_type = ent.studies
        if course_type == 'Licenta':
            if course_year == 1:
                subjects_list1.append(subjects_dict)
            if course_year == 2:
                subjects_list2.append(subjects_dict)
            if course_year == 3:
                subjects_list3.append(subjects_dict)
        else:
            if course_year == 1:
                subjects_list4.append(subjects_dict)
            if course_year == 2:
                subjects_list5.append(subjects_dict)

    data1["subjects"] = subjects_list1
    data2["subjects"] = subjects_list2
    data3["subjects"] = subjects_list3
    data4["subjects"] = subjects_list4
    data5["subjects"] = subjects_list5

    data_list.append(data1)
    data_list.append(data2)
    data_list.append(data3)
    data_list.append(data4)
    data_list.append(data5)

    json_data = json.dumps(data_list)
    return json_data


@hug.local()
@hug.get()
@hug.cli()
def courses_by_time(request, weekday: hug.types.text, start_hour: hug.types.number, end_hour: hug.types.number):
    """Retrieves all courses"""
    authorization = request.get_header('Authorization')
    if not authorization:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'No Authorization field exists in request header'}]}

    user_urlsafe = verify_token(authorization)
    if not user_urlsafe:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'Header contains token, but it is not a valid one.'}]}

    month, day, year = (int(x) for x in date.split('/'))
    date_obj = datetime.date(year, month, day)
    day_of_week = date_obj.weekday()

    # iau toate clasele (cursuri/lab)
    courses = get_classes(day_of_week)

    scheduled_classes_list = []
    for course in courses:
        if course.startHour == start_hour and course.endHour == end_hour:
            scheduled_classes_list.append(course)

    print(sheduled_classes_list)

    if not scheduled_classes_list:
        return {'status': 'error'}
    json_data = json.dumps(scheduled_classes_list)
    return json_data


@hug.local()
@hug.get()
@hug.cli()
def course(request, course_id: hug.types.text):
    """Retrieves course info"""
    authorization = request.get_header('Authorization')
    if not authorization:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'No Authorization field exists in request header'}]}

    user_urlsafe = verify_token(authorization)
    if not user_urlsafe:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'Header contains token, but it is not a valid one.'}]}

    course = Course.get(course_id)

    response = {}
    response["status"] = "ok"

    course_json = {}
    course_json["credits"] = str(course.credits)
    course_json["optional"] = "optional" if course.optional else "obligatoriu"
    course_json["studies"] = course.studies
    course_json["title"] = course.title
    course_json["year"] = str(course.year)

    if course.link:
        course_json["link"] = course.link
    if course.sub_desc:
        course_json["fisa"] = course.sub_desc

    response["course_info"] = course_json

    return response
