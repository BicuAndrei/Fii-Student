import ndb_orm as ndb

import Class

class Professor(ndb.Model):
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    type = ndb.StringProperty()
    teachingClass = ndb.KeyProperty(kind=Class, required=True)
