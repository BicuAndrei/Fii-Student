from fiistudentrest.models import Student, Course, ScheduleClass, ScheduleClassProfessor, Professor
from fiistudentrest.api_functions.auth import verify_token

import hug
import json
import datetime


def get_classes(day_of_the_week):
    """ Returneaza toate orele dintr-o anumita zi """
    query = ScheduleClass.query()
    query.add_filter('dayOfTheWeek', '=', day_of_the_week)
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

    student = Student.get(user_urlsafe)
    # iau toate clasele (cursuri/lab)
    sch_courses = get_classes(weekday)

    scheduled_classes_list = []
    data_list = []
    for sch_course in sch_courses:
        if sch_course.startHour == start_hour and sch_course.endHour == end_hour and sch_course.group[:2] == student.group[:2]:
            scheduled_classes_list.append(sch_course)
            
            try:
                course = Course.get(sch_course.course)
                course_title = course.title
            except:
                course_title = ''

            try:
                classroom = Classroom.get(sch_course.classroom)
                classroom_name = classroom.identifier
            except:
                print('A crapat classroom dupa cheie')
                classroom_name = ''

            try:
                sch_class_professor_query = ScheduleClassProfessor.query()
                sch_class_professor_query.add_filter(schedule_class,'=', sch_course.key)
                sch_class_professor_it = sch_class_professor_query.fetch()

                for sch_class_professor in sch_class_professor_it:
                    professor_key = sch_class_professor.professor
                    professor = Professor.get(professor_key)
                    professor_name = professor.firstName + ' ' + professor.lastName
            except:
                professor_name = ''

            if course_title != '':
                data = {'id': sch_course.urlsafe, 'type': sch_course.classType, 'title': course_title, 'classroom': classroom_name}
                data_list.append(data)

    return data_list


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
