import ndb_orm as ndb

class Announcement(ndb.Model):
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()