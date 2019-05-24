"""Sends mails via SendGrid."""

import pkg_resources

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ENCODING = "utf-8"


DEFAULT_MAIL="irinam.bejan@gmail.com"


def get_secret(name):
    content = pkg_resources.resource_string("fiistudentrest", f"secrets/{name}")
    return content.decode(ENCODING).strip()


def send_mail(from_mail, to_mails, subject, text_content, html_content=None):
    html_content = html_content or text_content
    message = Mail(
        from_email=from_mail,
        to_emails=to_mails,
        subject=subject,
        plain_text_content=text_content,
        html_content=html_content,
    )

    # added template
    message.template_id = '700c6c6a-8c12-4b7a-b4bc-5d8b2e8de06f'
    client = SendGridAPIClient(get_secret("sendgrid_key"))
    response = client.send(message)
    code = response.status_code
    was_successful = lambda ret_code: ret_code // 100 in (2, 3)
    if not was_successful(code):
        raise Exception("Couldn't send e-mail: {} {}".format(code, response.body))

    print("E-mail sent from", from_mail, " to ", to_mails, subject, code)
