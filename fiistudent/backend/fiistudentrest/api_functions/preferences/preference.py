import hug
from fiistudentrest.api_functions.auth import verify_token
from fiistudentrest.models import Student, Preference


@hug.put()
@hug.cli()
@hug.local()
def add_preference(request, preference: hug.types.text):
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
    newPref = Preference()
    newPref.student = student.key
    newPref.preference = preference
    newPref.put()
    return {'status': 'ok'}


if __name__ == '__main__':
    add_preference.interface.cli()
