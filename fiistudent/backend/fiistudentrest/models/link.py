from fiistudentrest.models.base import BaseModel, ndb

class Link(BaseModel):
    link = ndb.StringProperty()
    description = ndb.StringProperty()
