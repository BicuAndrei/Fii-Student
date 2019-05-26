from fiistudentrest.models import Classroom, ScheduleClass, Student, CustomClass
from fiistudentrest.api_functions.auth import verify_token

import hug
import datetime
import json


@hug.local()
@hug.put()
@hug.cli()
def add_custom_class(request, schedule_class_id: hug.types.text):
    """Adds custom schedule class for given user"""
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

    # getting the Student entity
    student = Student.get(user_urlsafe)
    schedule_class = ScheduleClass.get(schedule_class_id)

    # create the custom-class item
    custom_class = CustomClass(
        student = student.key,
        schedule_class = schedule_class.key
    )

    # store in db
    custom_class.put()

    return {'status':'ok'}
