import ndb_orm as ndb

class Course(ndb.Model):

    """Details about the course."""

    title = ndb.StringProperty()
    year = ndb.IntegerProperty()
    semester= ndb.IntegerProperty()
    credits = ndb.IntegerProperty()
    link = ndb.StringProperty()
