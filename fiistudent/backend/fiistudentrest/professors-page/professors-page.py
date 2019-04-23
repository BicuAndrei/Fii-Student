import hug
import json

from fiistudentrest.models import Professor


@hug.local()
@hug.get()
@hug.cli()
def professors():
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

    professors_list = []
    teached_subjects = []

    professors_query = Professor.query()
    professors_query_it = professors_query.fetch()

    for ent in professors_query_it:
        dictionary = {}
        dictionary["id"] = ent.urlsafe
        name = ent.firstName
        name += " " + ent.lastName
        dictionary["name"] = name
        dictionary["title"] = ent.type
        dictionary["office"] = ent.office
        dictionary["link"] = ent.link
        dictionary["teachedSubjects"] = teached_subjects

        professors_list.append(dictionary)

    json_data = json.dumps(professors_list)
    return json_data
