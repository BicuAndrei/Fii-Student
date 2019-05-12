from google.cloud import datastore
from fiistudentrest.models import Student
import hug
import phonenumbers
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
    if entity_exists(entity) == False:
        entity_key = entity.put()
        print("The key: ", entity_key)
        print(entity.email)
        return True
    return False


def is_real_number(phone_number):
    """ Verifies if a phone number is valid for Romania """
    the_phone_number = phonenumbers.parse(phone_number, "RO")
    return phonenumbers.is_valid_number_for_region(the_phone_number, "RO")


def hash_password(password):
    """ Encode a password """
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


@hug.get()
@hug.cli()
@hug.local()
def register(registrationNumber: hug.types.text, firstName: hug.types.text, lastName: hug.types.text,
             email: hug.types.text, phone_number: hug.types.text, password: hug.types.text,
             confirm_password: hug.types.text, year: hug.types.number,
             group: hug.types.text):
    """ Adds the entity in the datastore if possible and return an appropriate json response for every scenario """

    if len(firstName) < 3:
        return {'status': 'error',
                'errors': [
                    {'for': 'firstName', 'message': "The first name is not 3+ letters long."}]}
    elif len(lastName) < 3:
        return {'status': 'error',
                'errors': [
                    {'for': 'lastName', 'message': "The last name is not 3+ letters long."}]}
    elif len(password) < 6:
        return {'status': 'error',
                'errors': [
                    {'for': 'password', 'message': "The password is not 6+ characters long."}]}
    elif password != confirm_password:
        return {'status': 'error',
                'errors': [
                    {'for': 'confirm_password', 'message': "The password and the confirm password don't match."}]}
    elif is_real_number(phone_number) == False:
        return {'status': 'error',
                'errors': [{'for': 'phoneNumber', 'message': "The number is not valid."}]}
    else:
        # create the entity
        student = Student(
            registrationNumber=registrationNumber,
            firstName=firstName.capitalize(),
            lastName=lastName.capitalize(),
            email=email.lower(),
            phoneNumber=phone_number,
            password=hash_password(password),
            year=year,
            group=group.upper()
        )

        # add the entity if it does not exist and return a json response
        if register_function(student) == True:
            return {'status': 'ok', 'errors': []}
        else:
            return {'status': 'error', 'errors': [{'for': 'email', 'message': 'The email is already in our database.'}]}


if __name__ == '__main__':
    register.interface.cli()
