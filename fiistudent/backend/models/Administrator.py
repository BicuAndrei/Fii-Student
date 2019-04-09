import ndb_orm as ndb

class Administrator(ndb.Model):
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()