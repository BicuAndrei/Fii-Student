from fiistudentrest.models import Student
from fiistudentrest.utils.mail import send_mail, DEFAULT_MAIL

from itsdangerous import URLSafeSerializer, SignatureExpired
import hug


def entity_exists(email):
    """ Verify if the entity exists in the datastore """
    result = False
    query = Student.query()
    query.add_filter('email', '=', email)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            result = False
        else:
            result = True
    return result


def generate_token(email, salt='forgot-password'):
    serializer = URLSafeSerializer("Thisisasecret!!!")
    return serializer.dumps(email, salt)


def confirm_token(token):
    serializer = URLSafeSerializer("Thisisasecret!!!")
    try:
        email = serializer.loads(token, salt='forgot-password')
    except SignatureExpired:
        return False
    return email


def send_forgot_password_email(to_email):
    link = 'endpoint'
    token = generate_token(to_email)
    link_token = link + token

    subject = 'Change your password'
    content = '<body><h4>Hi there,</h4>' \
              '<p>This message is sent because you requested a change of password.</p>' \
              '<div style="display:flex; flex-direction: column; align-items: center">' \
              '<p>To change your password click on the button below.</p>' \
              '<a href="' + link_token + '" style="border: none;cursor: pointer;padding: 10px 20px;' \
                                         'border-radius: 5px;font-size: 15px; background-color: #21d146;' \
                                         'font-weight: bold; text-decoration:none; color:black">' \
                                         'Change your password</button>' \
                                         '</div></body>'
    send_mail(DEFAULT_MAIL, to_email, subject, content)


def forgot_password(email: hug.types.text):
    if entity_exists(email) == True:
        send_forgot_password_email(email)
        return {'status': 'ok'}
    else:
        return {'status': 'error', 'errors': [
            {'for': 'forgot_password', 'message': 'This email does not exist in our database'}]}


@hug.post()
@hug.cli()
@hug.local()
def confirm_forgot_password_token(token):
    """Checks whether the person has the email"""
    if confirm_token(token) != False:
        return {'status': 'ok'}
    else:
        return {'status': 'error', 'errors': [
            {'for': 'forgot_password', 'message': 'The link is invalid or has expired'}]}

