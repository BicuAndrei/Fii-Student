from fiistudentrest.models import Student
from fiistudentrest.utils.mail import send_mail, DEFAULT_MAIL

import hug
from itsdangerous import URLSafeSerializer, SignatureExpired

def send_confirm_email(to_email):
    link = "http://develop-dot-fii-student.appspot.com/confirm_email?token="
    token = generate_token(to_email)
    link_token = link + token
    print(link_token)

    subject = "Confirm your email"
    content = "<h4>Hi there,</h4>"
    content += "\n<p>This message is to confirm that the account created lately belongs to you. " \
               "Verifying your email address helps you secure your account. " \
               "If you forgot your password, you will now be able to reset it by email.</p>"
    content += '\n<div style="display:flex; flex-direction: column; align-items: center">'
    content += '\n<p>To confirm that this is your account press on the button below.</p>'
    content += '\n<a href="' + link_token + '">' \
               '\n<button style="border: none;cursor: pointer;padding: 10px 20px;border-radius: 5px;font-size: 15px;' \
               'background-color: #21d146;font-weight: bold">Confirm email</a></div>'

    send_mail(DEFAULT_MAIL, to_email, subject, content)


def generate_token(email, salt='email-confirmation'):
    serializer = URLSafeSerializer("Thisisasecret!!!")
    return serializer.dumps(email, salt)


def confirm_token(token):
    serializer = URLSafeSerializer("Thisisasecret!!!")
    try:
        email = serializer.loads(token, salt='email-confirmation')
    except SignatureExpired:
        return False
    return email


def confirm_email(token):
    """Sends confirmation email"""
    email = None
    try:
        email = confirm_token(token)
    except:
        return {'status': 'error', 'errors': [
            {'for': 'confirm_email', 'message': 'The confirmation link is invalid or has expired.'}]}
    query = Student.query()
    query.add_filter('email', '=', email)
    query_it = query.fetch()
    for ent in query_it:
        if ent.confirmed == True:
            print('You have confirmed your account.')
            return {'status': 'ok'}
        else:
            ent.confirmed = True
            Student.put(ent)
            print('Account already confirmed.')
            return {'status':'ok'}
