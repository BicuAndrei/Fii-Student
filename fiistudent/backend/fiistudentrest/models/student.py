import ndb_orm as ndb

class Student(ndb.Model):

    """Credentials and data of students."""

    registrationNumber = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    year = ndb.IntegerProperty()
    group = ndb.StringProperty()