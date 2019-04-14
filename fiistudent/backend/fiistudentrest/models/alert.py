from fiistudentrest.models.base import BaseModel, ndb

class Alert(BaseModel):
    type = ndb.StringProperty()
    level = ndb.StringProperty()
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()
