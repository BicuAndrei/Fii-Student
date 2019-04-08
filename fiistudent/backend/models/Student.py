import ndb_orm as ndb

class Student(ndb.Model):
    id = ndb.StringProperty()
    registrationNumber = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    year = ndb.IntegerProperty()
    group = ndb.StringProperty()