import ndb_orm as ndb

class Classroom(ndb.Model):

    """Location and capacity information of a classroom."""

    type = ndb.StringProperty()
    floor = ndb.IntegerProperty()
    identifier = ndb.StringProperty()
    capacity = ndb.IntegerProperty()
