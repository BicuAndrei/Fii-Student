from fiistudentrest.models.base import BaseModel, ndb

class Announcement(BaseModel):
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()