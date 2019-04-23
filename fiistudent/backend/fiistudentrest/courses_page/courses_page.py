import hug
import json

from fiistudentrest.models.course import Course
from fiistudentrest.auth import verify_token

@hug.local()
@hug.get()
@hug.cli()
def courses(request):
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
