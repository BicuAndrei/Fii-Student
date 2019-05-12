from fiistudentrest.models.base import BaseModel, ndb

class Student(BaseModel):

    """Credentials and data of students."""
    
    registrationNumber = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    phoneNumber = ndb.StringProperty()
    password = ndb.StringProperty()
    year = ndb.IntegerProperty()
    group = ndb.StringProperty()
    confirmed = ndb.BooleanProperty()