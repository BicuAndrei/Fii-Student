from fiistudentrest.models.base import BaseModel, ndb

class Student(BaseModel):

    """Credentials and data of students."""
    
    registrationNumber = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    year = ndb.IntegerProperty()
    group = ndb.StringProperty()