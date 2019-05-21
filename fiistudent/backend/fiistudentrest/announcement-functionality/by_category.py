import hug
import json

from fiistudentrest.models import Student, Announcement, Professor
from fiistudentrest.auth import verify_token


@hug.local()
@hug.get()
@hug.cli()
def get_announs_by_categ(request, category: hug.types.text):
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

    announcements = Announcement.query().add_filter('group', '=', student.group).add_filter('category','=',category).fetch()
    for ann in announcements:
        data = {'sender': ann.sender, 'text': ann.text, 'category': ann.category}
        data_list.append(data)

    json_data = json.dumps(data_list)
    return json_data

if __name__ == '__main__':
    get_announs_by_categ.interface.cli()