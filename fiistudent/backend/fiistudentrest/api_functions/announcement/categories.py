from fiistudentrest.api_functions.auth import verify_token
from fiistudentrest.models import Student, Announcement, Professor

import hug
import json


@hug.local()
@hug.get()
@hug.cli()
def get_announcements_by_categ(request, category: hug.types.text):
    """Retrieve all announcements given a category"""
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
    announcements_query.add_filter('category','=', category)
    announcements  = announcements_query.fetch()

    for ann in announcements:
        data = {'sender': ann.sender, 'subject':ann.subject, 'text': ann.text, 'category': ann.category}
        data_list.append(data)

    json_data = json.dumps(data_list)
    return json_data


@hug.get()
def get_categories(request):
    """Retrieves all categories for announcements"""
    
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

    categories = []
    announcements_query = Announcement.query()
    announcements_query.add_filter('group','=',student.group)
    announcements  = announcements_query.fetch()

    for ann in announcements:
        if ann.category:
            categories.append(ann.category)

    categories = list(dict.fromkeys(categories))
    return {'status':'ok','categories':categories}
