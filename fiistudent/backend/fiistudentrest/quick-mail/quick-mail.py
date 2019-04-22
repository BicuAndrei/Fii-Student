import fiistudentrest.mail as Mail
from fiistudentrest.models import Student
from fiistudentrest.models import Professor
import hug


def exists(email, user_type):
    """ Verify if the user exists in the datastore """
    result = False
    query = user_type.query()
    query.add_filter('email', '=', email)
    print(query)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            print('The user is not in our database.')
            result = False
        else:
            print('The user exists in our database.')
            result = True
    return result


@hug.local()
@hug.get()
@hug.cli()
def send_email(from_email: hug.types.text, urlsafe: hug.types.text, subject: hug.types.text, content: hug.types.text):
    """ Sends an email from a student to a professor """
    professor = Professor.get(urlsafe)
    if exists(from_email, Student) == True and exists(professor.email, Professor) == True:
        Mail.send_mail(from_email, professor.email, subject, content)
        return {'status': 'ok', 'errors': []}
    elif exists(from_email, Student) == True and exists(professor.email, Professor) == False:
        return {'status': 'error',
                'errors': [
                    {'for': 'email_professor', 'message': 'We could not find the professor with the email({}).'.format(professor.email)}]}
    elif exists(from_email, Student) == False and exists(professor.email, Professor) == True:
        return {'status': 'error',
                'errors': [
                    {'for': 'email_student', 'message': 'We could not find the student with the email({}).'.format(from_email)}]}
    else:
        return {'status': 'error', 'errors': [
            {'for': 'email_student', 'message': 'We could not find the student with the email({}).'.format(from_email)},
            {'for': 'email_professor', 'message': 'We could not find the professor with the email({}).'.format(to_email)}]}
