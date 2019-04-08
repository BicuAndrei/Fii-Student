import ndb_orm as ndb

class Administrator(ndb.Model):
    id = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()