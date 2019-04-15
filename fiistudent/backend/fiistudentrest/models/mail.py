from fiistudentrest.models.base import BaseModel, ndb

class Mail(BaseModel):

    """Subject and receiver of the email."""
    
    cc = ndb.StringProperty()
    bcc = ndb.StringProperty()
    subject = ndb.StringProperty()