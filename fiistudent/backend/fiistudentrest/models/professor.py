import ndb_orm as ndb

from . import Course

class Professor(ndb.Model):

    """Credentials and data of professor."""

    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    type = ndb.StringProperty()
    teachingClass = ndb.KeyProperty(kind=Course, required=True)
