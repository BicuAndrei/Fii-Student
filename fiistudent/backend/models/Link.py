import ndb_orm as ndb

class Link(ndb.Model):
    id = ndb.StringProperty()
    link = ndb.StringProperty()
    description = ndb.StringProperty()
