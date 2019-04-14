import ndb_orm as ndb

class Alert(BaseModel):
    type = ndb.StringProperty()
    level = ndb.StringProperty()
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()