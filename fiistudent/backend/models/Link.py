import ndb_orm as ndb

class Link(ndb.Model):
    link = ndb.StringProperty()
    description = ndb.StringProperty()
