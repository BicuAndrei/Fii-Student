from google.cloud import datastore
from fiistudentrest.models import Professor
import fiistudentrest.mail as Mail
from .confirm_email import send_confirm_email as send_confirmation_email
import hug
import uuid
import hashlib


def get_professor_by_email(email):
    """ Gets professor from database by email"""
    query = Professor.query()
    query.add_filter('email', '=', email)
    print(query)
    query_it = query.fetch()
    for ent in query_it:
        if ent is not None:
            print(ent)
            return ent
    return None


def hash_password(password):
    """ Encode a password """
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


@hug.put()
@hug.cli()
@hug.local()
def register(first_name: hug.types.text, last_name: hug.types.text, professor_type: hug.types.text,
             email: hug.types.text, password: hug.types.text, confirm_password: hug.types.text):
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
            firstName=first_name.capitalize(),
            lastName=last_name.capitalize(),
            type=professor_type,
            email=email.lower(),
            password=hash_password(password),
            confirmed=False
        )
        # get professor by email from the database
        professor_db = get_professor_by_email(email)
        if professor_db is not None:
            # if entity with this mail already exists, update all fields
            professor_db.firstName = professor.firstName
            professor_db.lastName = professor.lastName
            professor_db.type = professor.type
            professor_db.email = professor.email
            professor_db.password = professor.password
            professor_db.confirmed = False
            entity_key = Professor.put(professor_db)
        else:
            # add new professor entity to the database
            entity_key = Professor.put(professor)

        print("The key: ", entity_key)
        print(professor.email)

        # send confirmation email
        send_confirmation_email(email)
        return {'status': 'ok', 'errors': []}


if __name__ == '__main__':
    register.interface.cli()
