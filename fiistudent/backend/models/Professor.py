import ndb_orm as ndb

class Professor(ndb.Model):
    id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    type = ndb.StringProperty()
    id_class = ndb.StringProperty()
