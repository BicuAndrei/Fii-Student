import hug
import json

from fiistudentrest.models import Professor, Feedback
from fiistudentrest.api_functions.auth import verify_token


@hug.local()
@hug.get()
@hug.cli()
def get_feedback_by_professor(request):
    """Retrieves all feedback for current logged in professor"""
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
    professor = Professor.get(user_urlsafe)
    # filter feedback by professor
    query = Feedback.query()
    query.add_filter('professor', '=', professor.urlsafe)
    query_it = query.fetch()
    data_list = []
    for ent in query_it:

        course_title = Course.get(ent.course).title
        
        data = {'stars': ent.stars, 'feedback': ent.text, 'date': ent.created_at, 'course': course_title}
        data_list.append(data)

    return data_list
