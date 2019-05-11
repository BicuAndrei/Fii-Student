from fiistudentrest.models import Student
from fiistudentrest.auth import verify_token
import hug


@hug.local()
@hug.get()
@hug.cli()
def change_group(request, user_urlsafe: hug.types.text, semian: hug.types.text, group: hug.types.text):
    """ Changes the group for a student and returns a json response for every case"""
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
    new_group = semian + group
    print("The new group for the student " + student.key + " is " + new_group)
    student.group = new_group
    Student.put(student)
    print("The modification is done!")

    return {'status': 'ok',
            'errors': []}


if __name__ == '__main__':
    change_group.interface.cli()
