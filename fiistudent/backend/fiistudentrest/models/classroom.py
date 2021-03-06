from fiistudentrest.models.base import BaseModel, ndb

class Classroom(BaseModel):
    
    """Location and capacity information of a classroom."""

    type = ndb.StringProperty()
    floor = ndb.IntegerProperty()
    identifier = ndb.StringProperty()
    capacity = ndb.IntegerProperty()
