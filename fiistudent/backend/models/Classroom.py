import ndb_orm as ndb

class Classroom(ndb.Model):
    id = ndb.StringProperty()
    type = ndb.StringProperty()
    floor = ndb.IntegerProperty()
    identifier = ndb.StringProperty()
    capacity = ndb.IntegerProperty()
