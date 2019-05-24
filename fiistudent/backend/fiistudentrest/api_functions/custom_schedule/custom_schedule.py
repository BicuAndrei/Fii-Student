from fiistudentrest.models import Classroom, ScheduleClass
from fiistudentrest.api_functions.auth import verify_token

import hug
import datetime
import json


@hug.local()
@hug.put()
@hug.cli()
def add_custom_class(request, weekday: hug.types.text, start_hour: hug.types.number, end_hour: hug.types.number, schedule_class_id: hug.types.text):
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

    return {'status':'ok'}
