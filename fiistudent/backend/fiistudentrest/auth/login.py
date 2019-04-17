from google.cloud import datastore
from fiistudentrest.models import Student
import hug


def login_function(email, password):
    """ Verify if the user exists in the datastore """
    result = False
    query = Student.query()
    query.add_filter('email', '=', email)
    query.add_filter('password', '=', password)
    print(query)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            print('The user is not in our database or introduced the wrong credentials.')
            result = False
        else:
            print('The user exists in our database.')
            result = True
    return result


@hug.local()
@hug.cli()
@hug.get()
def login(email: hug.types.text, password: hug.types.text):
    """ Verify if the user exists in the datastore and return an appropriate json response for every scenario """
    if login_function(email, password) == True:
        return {'status': 'ok', 'errors': []}
    else:
        return {'status': 'error', 'errors': [
            {'for': 'login', 'message': 'The username or password you entered did not match our records.'}]}
