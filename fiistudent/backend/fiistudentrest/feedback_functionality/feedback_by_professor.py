import hug
import json

from fiistudentrest.models import Professor
from fiistudentrest.models.feedback import Feedback
from fiistudentrest.auth import verify_token


@hug.local()
@hug.get()
@hug.cli()
def get_feedback_by_professor(request):
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
    query.add_filter('professor', '=', professor)
    query_it = query.fetch()
    data_list = []
    for ent in query_it:
        data = {'stars': ent.stars, 'feedback': ent.text, 'date': ent.created_at, 'course': ent.course}
        data_list.append(data)

    json_data = json.dumps(data_list)
    return json_data
