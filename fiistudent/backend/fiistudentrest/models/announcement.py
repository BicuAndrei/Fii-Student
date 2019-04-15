import ndb_orm as ndb

class Announcement(ndb.Model):

    """The name of the person who puts the announcement and for whom it is intended."""

    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()