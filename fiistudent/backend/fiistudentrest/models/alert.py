from fiistudentrest.models.base import BaseModel, ndb

class Alert(BaseModel):

    """Information about an alert (who gave it, how serious it is, who it's intended for)."""

    type = ndb.StringProperty()
    level = ndb.StringProperty()
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()
