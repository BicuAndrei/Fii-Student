from fiistudentrest.models.base import BaseModel, ndb
from .professor import Professor


class Announcement(BaseModel):

    """The name of the person who puts the announcement and for whom it is intended."""

    sender = ndb.KeyProperty(kind=Professor)
    receiver = ndb.StringProperty()
    subject = ndb.StringProperty()
    text = ndb.StringProperty()
    category = ndb.StringProperty()
