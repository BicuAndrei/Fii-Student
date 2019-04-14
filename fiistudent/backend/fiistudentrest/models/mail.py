from fiistudentrest.models.base import BaseModel, ndb

class Mail(BaseModel):
    cc = ndb.StringProperty()
    bcc = ndb.StringProperty()
    subject = ndb.StringProperty()