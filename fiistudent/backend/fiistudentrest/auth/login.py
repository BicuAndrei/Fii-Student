from google.cloud import datastore
from fiistudentrest.models import Student

import hug
import jwt

from datetime import datetime, timedelta

config = {
    'jwt_secret': 'super-secret-key-please-change',
    # Token will expire in 3600 seconds if it is not refreshed and the user will be required to log in again.
    'token_expiration_seconds': 3600,
    # If a request is made at a time less than 1000 seconds before expiry, a new jwt is sent in the response header.
    'token_refresh_seconds': 1000, 
    'jwt_algorithm': 'HS256'
}


def login_function(email, password):
    """ Verify if the user exists in the datastore """
    query = Student.query()
    query.add_filter('email', '=', email)
    query.add_filter('password', '=', password)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            print('The user is not in our database or introduced the wrong credentials.')
        else:
            print('The user exists in our database.')
            return ent.urlsafe
    return None


@hug.local()
@hug.cli()
@hug.get()
def login(email: hug.types.text, password: hug.types.text):
    """ Verify if the user exists in the datastore and return an appropriate json response for every scenario """
    user_url = login_function(email, password)
    if user_url != None:
        payload = {
            'user_url': user_url,
            'exp': datetime.utcnow() + timedelta(seconds=config['token_expiration_seconds'])
        }
        jwt_token = jwt.encode(payload, config['jwt_secret'], config['jwt_algorithm'])
        return {'token': jwt_token.decode("utf-8"), 'errors': []}
    else:
        return {'status': 'error', 'errors': [
            {'for': 'login', 'message': 'The username or password you entered did not match our records.'}]}


if __name__ == '__main__':
    
    login.interface.cli()
