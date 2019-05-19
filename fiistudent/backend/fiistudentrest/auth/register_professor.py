from google.cloud import datastore
from fiistudentrest.models import Professor
import fiistudentrest.mail as Mail
from .confirm_email import send_confirm_email as send_confirmation_email
import hug
import uuid
import hashlib


def entity_exists(entity):
    """ Verify if the entity exists in the datastore """
    result = False
    query = entity.query()
    query.add_filter('email', '=', entity.email)
    print(query)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            print('The entity {} will be added.'.format(entity))
            result = False
        else:
            print('The entity exists.')
            result = True
    return result


def register_function(entity):
    """ Adds the entity in the datastore """
    if not entity_exists(entity):
        entity_key = entity.put()
        print("The key: ", entity_key)
        print(entity.email)
        return True
    return False


def hash_password(password):
    """ Encode a password """
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


@hug.get()
@hug.cli()
@hug.local()
def register(registration_number: hug.types.text, first_name: hug.types.text, last_name: hug.types.text,
             professor_type: hug.types.text, email: hug.types.text, password: hug.types.text,
             confirm_password: hug.types.text):
    """ Adds the entity in the datastore if possible and return an appropriate json response for every scenario """
    if len(first_name) < 3:
        return {'status': 'error',
                'errors': [
                    {'for': 'first_name', 'message': "The first name is not 3+ letters long."}]}
    elif len(last_name) < 3:
        return {'status': 'error',
                'errors': [
                    {'for': 'last_name', 'message': "The last name is not 3+ letters long."}]}
    elif len(password) < 6:
        return {'status': 'error',
                'errors': [
                    {'for': 'password', 'message': "The password is not 6+ characters long."}]}
    elif password != confirm_password:
        return {'status': 'error',
                'errors': [
                    {'for': 'confirm_password', 'message': "The password and the confirm password don't match."}]}
    elif not email.lower().endswith("@info.uaic.ro"):
        return {'status': 'error',
                'errors': [{'for': 'email', 'message': "The email address is not @info.uaic.ro"}]}
    else:
        # create entity
        professor = Professor(
            registrationNumber=registration_number,
            firstName=first_name.capitalize(),
            lastName=last_name.capitalize(),
            type=professor_type,
            email=email.lower(),
            password=hash_password(password),
            confirmed=False
        )

        # add the entity if it does not exist and return a json response
        if register_function(professor):
            # send confirmation email
            send_confirmation_email(email)
            return {'status': 'ok', 'errors': []}
        else:
            return {'status': 'error', 'errors': [{'for': 'email', 'message': 'The email is already in our database.'}]}


if __name__ == '__main__':
    register.interface.cli()
