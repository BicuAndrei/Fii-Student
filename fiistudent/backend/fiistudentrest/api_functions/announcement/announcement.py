from fiistudentrest.api_functions.auth import verify_token
from fiistudentrest.models import Student, Professor, Announcement

import hug
import json


@hug.local()
@hug.get()
@hug.cli()
def get_announs(request):
    """Retrieve all announcements by current student's group"""
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

    data_list = []

    announcements_query = Announcement.query()
    announcements_query.add_filter('group','=',student.group)
    announcements  = announcements_query.fetch()
    for ann in announcements:
        data = {'sender': ann.sender, 'subject':ann.subject,'text':ann.text, 'category':ann.category}
        data_list.append(data)


    return data_list


@hug.local()
@hug.put()
@hug.cli()
def add_new_announcement(request, subject:hug.types.text, group: hug.types.text, text: hug.types.text, category: hug.types.text):
    """Add new announcement"""
    authorization = request.get_header('Authorization')
    if not authorization:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'No Authorization field exists in request header'}]}

    professor_key_urlsafe = verify_token(authorization)
    if not professor_key_urlsafe:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'Header contains token, but it is not a valid one.'}]}
    
    professor = Professor.get(professor_key_urlsafe)

    announcement = Announcement(
        sender=professor.key,
        receiver=group,
        subject=subject,
        text=text,
        category=category
    )

    announcement.put()

    return {'status': 'ok'}
