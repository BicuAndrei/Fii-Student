from fiistudentrest.models.base import BaseModel, ndb

class Announcement(BaseModel):

    """The name of the person who puts the announcement and for whom it is intended."""

    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()