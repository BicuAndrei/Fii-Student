from fiistudentrest.models.base import BaseModel, ndb

class Classroom(BaseModel):
    type = ndb.StringProperty()
    floor = ndb.IntegerProperty()
    identifier = ndb.StringProperty()
    capacity = ndb.IntegerProperty()
