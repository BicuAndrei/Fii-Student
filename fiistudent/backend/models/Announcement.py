import ndb_orm as ndb

class Announcement(ndb.Model):
    id = ndb.StringProperty()
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()