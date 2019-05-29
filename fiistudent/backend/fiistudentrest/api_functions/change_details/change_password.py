from fiistudentrest.models import Student
from fiistudentrest.api_functions.auth import verify_token

import hug
import uuid
import hashlib


def hash_password(password):
    """Encode a password """
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    """Decode a password """
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


@hug.local()
@hug.post()
@hug.cli()
def change_password(request, old_password: hug.types.text, new_password: hug.types.text,
                    confirm_password: hug.types.text):
    """Changes the password for a student and returns a json response"""
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
    # verifies
    if not check_password(student.password, old_password):
        return {'status': 'error',
                'errors': [
                    {'for': 'old_password', 'message': "This is not the old password."}]}
    elif len(new_password) < 6:
        return {'status': 'error',
                'errors': [
                    {'for': 'new_password', 'message': "The new password is not 6+ characters long."}]}
    elif new_password != confirm_password:
        return {'status': 'error',
                'errors': [
                    {'for': 'confirm_password', 'message': "The new password and the confirm password don't match."}]}

    student.password = hash_password(new_password)
    print("The new password for the student " + str(student.urlsafe) + " is " + hash_password(new_password))
    Student.put(student)
    print("The modification is done!")

    return {'status': 'ok',
            'errors': []}


if __name__ == '__main__':
    change_password.interface.cli()
