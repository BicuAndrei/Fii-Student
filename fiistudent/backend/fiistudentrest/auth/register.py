from google.cloud import datastore
from fiistudentrest.models import Student
import hug


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


@hug.get()
@hug.cli()
@hug.local()
def register(registrationNumber: hug.types.text, firstName: hug.types.text, lastName: hug.types.text,
             email: hug.types.text, username: hug.types.text, password: hug.types.text,
             confirm_password: hug.types.text, year: hug.types.number,
             group: hug.types.text, hug_timer=3):
    """ Adds the entity in the datastore if possible and return an appropriate json response for every scenario """
    # verify if the password and confirm password match, if they don't match, return a json response
    if password != confirm_password:
        return {'status': 'error',
                'errors': [{'for': 'confirm_password', 'message': "The password and the confirm password don't match"}]}
    else:
        # create the entity

        student = Student(
            registrationNumber=registrationNumber,
            firstName=firstName,
            lastName=lastName,
            email=email.lower(),
            username=username,
            password=password,
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