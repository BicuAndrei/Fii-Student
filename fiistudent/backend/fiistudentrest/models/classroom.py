import ndb_orm as ndb

class Classroom(BaseModel):
    type = ndb.StringProperty()
    floor = ndb.IntegerProperty()
    identifier = ndb.StringProperty()
    capacity = ndb.IntegerProperty()
