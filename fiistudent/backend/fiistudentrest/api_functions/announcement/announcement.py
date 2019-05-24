from fiistudentrest.auth import verify_token
from fiistudentrest.models import Professor, Announcement

import hug

@hug.local()
@hug.put()
@hug.cli()
def add_new_announcement(request, group: hug.types.text, text: hug.types.text, category: hug.types.text):
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
        text=text,
        category=category
    )
    announcement.put()
