import os
from twilio.rest import Client
import hug
import pkg_resources

ENCODING = "utf-8"


def get_secret(name):
    content = pkg_resources.resource_string("fiistudentrest", f"secrets/{name}")
    return content.decode(ENCODING).strip()


account_sid = get_secret("twilio_sid")
auth_token = get_secret("twilio_token")
client = Client(account_sid, auth_token)


@hug.get()
@hug.cli()
@hug.local()
def send_sms(to: hug.types.text, body: hug.types.text):
    message = client.messages \
        .create(
        body=body,
        from_='+19384448986',
        to= "+4" + to
    )


if __name__ == '__main__':
    send_sms.interface.cli()
