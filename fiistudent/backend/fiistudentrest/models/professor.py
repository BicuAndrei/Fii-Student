from fiistudentrest.models.base import BaseModel, ndb

from . import Course

class Professor(BaseModel):
    
    """Credentials and data of professor."""

    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    type = ndb.StringProperty()
    office = ndb.StringProperty()
    link = ndb.StringProperty()
