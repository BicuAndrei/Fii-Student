import os

from fiistudentrest.auth import verify_token
from fiistudentrest.models import Professor

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\gabil\\Documents\\fii-student-5c3ee6b54bbd.json"
print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

import hug

@hug.local()
@hug.get()
@hug.cli()
def add_new_announcement(request, group: hug.types.text, text: hug.types.text):
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


if __name__ == '__main__':
    add_new_announcement.interface.cli()
