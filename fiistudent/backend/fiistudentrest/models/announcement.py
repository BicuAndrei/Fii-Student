from fiistudentrest.models import Professor
from fiistudentrest.models.base import BaseModel, ndb


class Announcement(BaseModel):

    """The name of the person who puts the announcement and for whom it is intended."""

    sender = ndb.StringProperty(kind=Professor)
    receiver = ndb.StringProperty()
    text = ndb.StringProperty()
    category = ndb.StringProperty()
