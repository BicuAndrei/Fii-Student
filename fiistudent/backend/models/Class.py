import ndb_orm as ndb

class Class(ndb.Model):
    id = ndb.StringProperty()
    title = ndb.StringProperty()
    year = ndb.IntegerProperty()
    semester= ndb.IntegerProperty()
    credits = ndb.IntegerProperty()
    link = ndb.StringProperty()
